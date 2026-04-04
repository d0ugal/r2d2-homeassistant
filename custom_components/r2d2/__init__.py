"""The R2D2 integration."""

from __future__ import annotations

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_MAC, DOMAIN, LED_MAX, MOTOR_SPEED_DEFAULT

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

_SCHEMA_MOVE = vol.Schema(
    {
        vol.Required("direction"): vol.In([
            "forward", "reverse", "left", "right",
            "forward_left", "forward_right", "reverse_left", "reverse_right",
        ]),
        vol.Required("move_for"): vol.All(vol.Coerce(float), vol.Range(min=0.1, max=30)),
        vol.Optional("speed"): vol.All(int, vol.Range(min=0, max=3)),
    }
)
_SCHEMA_STOP = vol.Schema({})
_SCHEMA_PLAY_SOUND = vol.Schema(
    {
        vol.Required("sound"): str,
    }
)
_SCHEMA_SET_HEAD = vol.Schema(
    {
        vol.Required("position"): vol.In(["left", "center", "right"]),
    }
)
_SCHEMA_SET_LEDS = vol.Schema(
    {
        vol.Optional("blue"): vol.All(int, vol.Range(min=0, max=LED_MAX)),
        vol.Optional("red"): vol.All(int, vol.Range(min=0, max=LED_MAX)),
    }
)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    from .coordinator import R2D2Coordinator

    hass.data.setdefault(DOMAIN, {})

    coordinator = R2D2Coordinator(hass, entry)
    await coordinator.async_connect()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    def _coordinators():
        return [
            c
            for c in hass.data.get(DOMAIN, {}).values()
            if isinstance(c, R2D2Coordinator)
        ]

    async def _move(call) -> None:
        speed = call.data.get("speed", MOTOR_SPEED_DEFAULT)
        for coord in _coordinators():
            await coord.do_move(call.data["direction"], call.data["move_for"], speed)

    async def _stop(call) -> None:
        for coord in _coordinators():
            await coord.do_stop()

    async def _play_sound(call) -> None:
        for coord in _coordinators():
            await coord.do_play_sound(call.data["sound"])

    async def _set_head(call) -> None:
        for coord in _coordinators():
            await coord.do_set_head(call.data["position"])

    async def _set_leds(call) -> None:
        for coord in _coordinators():
            await coord.do_set_leds(
                blue=call.data.get("blue"),
                red=call.data.get("red"),
            )

    if not hass.services.has_service(DOMAIN, "move"):
        hass.services.async_register(DOMAIN, "move", _move, _SCHEMA_MOVE)
        hass.services.async_register(DOMAIN, "stop", _stop, _SCHEMA_STOP)
        hass.services.async_register(DOMAIN, "play_sound", _play_sound, _SCHEMA_PLAY_SOUND)
        hass.services.async_register(DOMAIN, "set_head", _set_head, _SCHEMA_SET_HEAD)
        hass.services.async_register(DOMAIN, "set_leds", _set_leds, _SCHEMA_SET_LEDS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    from .coordinator import R2D2Coordinator

    coordinator = hass.data.get(DOMAIN, {}).get(entry.entry_id)
    if coordinator:
        coordinator.cancel_move()
        await coordinator.async_disconnect()

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    if not any(
        isinstance(c, R2D2Coordinator) for c in hass.data.get(DOMAIN, {}).values()
    ):
        for svc in ("move", "stop", "play_sound", "set_head", "set_leds"):
            hass.services.async_remove(DOMAIN, svc)

    return unload_ok
