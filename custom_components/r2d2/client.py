"""Low-level BLE client for the Clementoni R2D2 remote-control droid.

Protocol: 20-byte write to UUID_WRITE, no response required.

Packet layout (confirmed by ARM64 disassembly of libil2cpp.so):
  [0]    0xB5  header
  [1]    snd   sound effect (momentary; 0x00 = silent)
  [2]    0x00  padding
  [3]    mt1   motor-1 direction (0=stop, 1=fwd, 2=rev)
  [4]    sp1   motor-1 speed (0-3)
  [5]    mt2   motor-2 direction
  [6]    sp2   motor-2 speed
  [7]    hed   head position (0x04=left … 0x14=center … 0x24=right)
  [8]    ldb   first LED unit — green/blue channel (0-3)
  [9]    ldr   first LED unit — red channel (0-3)
  [10]   ldb   second LED unit — green/blue channel (mirror of [8])
  [11]   ldr   second LED unit — red channel (mirror of [9])
  [12-19]      fixed tail: 7C 6B 5A 49 38 27 16 05

  Note: the hardware has two bicolour (red/green) LED units. The app
  labels the green channel "blue" because R2-D2 is blue. Both units
  are driven identically so all four bytes are always set.
"""

from __future__ import annotations

import logging

from bleak import BleakClient
from bleak_retry_connector import establish_connection

from .const import (
    HEAD_CENTER,
    MOTOR_SPEED_DEFAULT,
    MOTOR_STOP,
    PACKET_FIXED_TAIL,
    PACKET_HEADER,
    UUID_WRITE,
)

_LOGGER = logging.getLogger(__name__)


def build_packet(
    sound: int = 0x00,
    mt1: int = MOTOR_STOP,
    sp1: int = MOTOR_SPEED_DEFAULT,
    mt2: int = MOTOR_STOP,
    sp2: int = MOTOR_SPEED_DEFAULT,
    head: int = HEAD_CENTER,
    led_blue: int = 0x00,
    led_red: int = 0x00,
) -> bytes:
    body = bytes(
        [
            PACKET_HEADER,
            sound,
            0x00,
            mt1,
            sp1,
            mt2,
            sp2,
            head,
            led_blue,
            led_red,  # first LED unit (green/blue + red)
            led_blue,
            led_red,  # second LED unit (mirror)
        ]
    )
    return body + PACKET_FIXED_TAIL


class R2D2Client:
    """Manages the BLE connection and packet dispatch for R2D2."""

    def __init__(self, address: str) -> None:
        self._address = address
        self._client: BleakClient | None = None

    @property
    def is_connected(self) -> bool:
        return self._client is not None and self._client.is_connected

    async def connect(self, ble_device=None) -> None:
        if self.is_connected:
            return
        _LOGGER.debug("Connecting to R2D2 at %s", self._address)
        if ble_device is not None:
            self._client = await establish_connection(
                BleakClient, ble_device, self._address
            )
        else:
            client = BleakClient(self._address)
            self._client = client
            await client.connect()
        _LOGGER.debug("Connected to R2D2")

    async def disconnect(self) -> None:
        if self._client:
            try:
                await self._client.disconnect()
            except Exception:
                pass
            self._client = None

    async def send(self, packet: bytes) -> None:
        if not self.is_connected:
            _LOGGER.warning("R2D2 not connected — skipping send")
            return
        try:
            assert self._client is not None
            await self._client.write_gatt_char(UUID_WRITE, packet, response=False)
        except Exception as exc:
            _LOGGER.error("Failed to send packet to R2D2: %s", exc)
            self._client = None
            raise
