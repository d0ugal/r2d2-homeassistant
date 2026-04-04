"""Coordinator for the R2D2 integration — state management and BLE dispatch."""

from __future__ import annotations

import asyncio
import logging

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .client import R2D2Client, build_packet
from .const import (
    CONF_MAC,
    DOMAIN,
    HEAD_CENTER,
    HEAD_POSITIONS,
    LED_MAX,
    MOTOR_FORWARD,
    MOTOR_REVERSE,
    MOTOR_SPEED_DEFAULT,
    MOTOR_STOP,
    SOUNDS,
)

_LOGGER = logging.getLogger(__name__)


class R2D2Coordinator(DataUpdateCoordinator):
    """Holds R2D2 state and dispatches BLE packets on change."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(hass, _LOGGER, name=DOMAIN)
        self._entry = entry
        self._client = R2D2Client(entry.data[CONF_MAC])
        self._move_task: asyncio.Task | None = None

        # Current state
        self._head: int = HEAD_CENTER
        self._led_blue: int = 0x00
        self._led_red: int = 0x00

    @property
    def is_connected(self) -> bool:
        return self._client.is_connected

    async def _async_update_data(self) -> dict:
        return {"connected": self._client.is_connected}

    async def async_connect(self) -> None:
        address = self._entry.data[CONF_MAC]
        ble_device = bluetooth.async_ble_device_from_address(self.hass, address)
        try:
            await self._client.connect(ble_device)
        except Exception as exc:
            _LOGGER.warning("Could not connect to R2D2: %s", exc)
        self.async_set_updated_data({"connected": self._client.is_connected})

    async def async_disconnect(self) -> None:
        self.cancel_move()
        await self._client.disconnect()

    # ------------------------------------------------------------------
    # Move management
    # ------------------------------------------------------------------

    def cancel_move(self) -> None:
        if self._move_task and not self._move_task.done():
            self._move_task.cancel()
        self._move_task = None

    async def do_move(
        self,
        direction: str,
        move_for: float,
        speed: int = MOTOR_SPEED_DEFAULT,
    ) -> None:
        """Start moving in direction for move_for seconds, then stop.

        direction: "forward" | "reverse" | "left" | "right"
        """
        self.cancel_move()
        if not self.is_connected:
            await self.async_connect()

        mt1, mt2 = _direction_to_motors(direction)
        self._move_task = self.hass.async_create_task(
            self._run_move(mt1, mt2, speed, move_for)
        )

    async def _run_move(
        self, mt1: int, mt2: int, speed: int, duration: float
    ) -> None:
        packet = build_packet(
            mt1=mt1, sp1=speed, mt2=mt2, sp2=speed,
            head=self._head, led_blue=self._led_blue, led_red=self._led_red,
        )
        try:
            await self._client.send(packet)
            await asyncio.sleep(duration)
        except asyncio.CancelledError:
            pass
        finally:
            self._move_task = None
            await self._send_stop()

    async def do_stop(self) -> None:
        self.cancel_move()
        if not self.is_connected:
            await self.async_connect()
        await self._send_stop()

    async def _send_stop(self) -> None:
        packet = build_packet(
            mt1=MOTOR_STOP, sp1=0, mt2=MOTOR_STOP, sp2=0,
            head=self._head, led_blue=self._led_blue, led_red=self._led_red,
        )
        try:
            await self._client.send(packet)
        except Exception as exc:
            _LOGGER.warning("Failed to send stop: %s", exc)

    # ------------------------------------------------------------------
    # Sound
    # ------------------------------------------------------------------

    async def do_play_sound(self, sound: str) -> None:
        if not self.is_connected:
            await self.async_connect()
        sound_id = SOUNDS.get(sound, 0x00)
        packet = build_packet(
            sound=sound_id,
            head=self._head, led_blue=self._led_blue, led_red=self._led_red,
        )
        await self._client.send(packet)
        # Send a follow-up packet with sound=0 so the sound plays once
        await asyncio.sleep(0.2)
        packet = build_packet(
            head=self._head, led_blue=self._led_blue, led_red=self._led_red,
        )
        await self._client.send(packet)

    # ------------------------------------------------------------------
    # Head
    # ------------------------------------------------------------------

    async def do_set_head(self, position) -> None:
        if not self.is_connected:
            await self.async_connect()
        try:
            # Accept raw byte value (4–36) for fine-grained control
            self._head = max(HEAD_LEFT, min(HEAD_RIGHT, int(position)))
        except (ValueError, TypeError):
            self._head = HEAD_POSITIONS.get(str(position), HEAD_CENTER)
        packet = build_packet(
            head=self._head, led_blue=self._led_blue, led_red=self._led_red,
        )
        await self._client.send(packet)

    # ------------------------------------------------------------------
    # LEDs
    # ------------------------------------------------------------------

    async def do_set_leds(
        self,
        blue: int | None = None,
        red: int | None = None,
    ) -> None:
        if not self.is_connected:
            await self.async_connect()
        if blue is not None:
            self._led_blue = max(0, min(LED_MAX, blue))
        if red is not None:
            self._led_red = max(0, min(LED_MAX, red))
        packet = build_packet(
            head=self._head, led_blue=self._led_blue, led_red=self._led_red,
        )
        await self._client.send(packet)
        self.async_set_updated_data({"connected": self._client.is_connected})


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _direction_to_motors(direction: str) -> tuple[int, int]:
    """Return (mt1, mt2) motor direction bytes for a given movement direction.

    Cardinal directions run both motors equally.
    Diagonal directions stop one motor so the robot curves; the active
    motor still runs at the caller-supplied speed.
    """
    return {
        "forward":       (MOTOR_FORWARD,  MOTOR_FORWARD),
        "reverse":       (MOTOR_REVERSE,  MOTOR_REVERSE),
        "left":          (MOTOR_REVERSE,  MOTOR_FORWARD),
        "right":         (MOTOR_FORWARD,  MOTOR_REVERSE),
        "forward_left":  (MOTOR_STOP,     MOTOR_FORWARD),
        "forward_right": (MOTOR_FORWARD,  MOTOR_STOP),
        "reverse_left":  (MOTOR_STOP,     MOTOR_REVERSE),
        "reverse_right": (MOTOR_REVERSE,  MOTOR_STOP),
    }.get(direction, (MOTOR_STOP, MOTOR_STOP))
