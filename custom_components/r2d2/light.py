"""Light platform for R2D2 — bicolour LED control.

The hardware has two identical bicolour (red/green) LED units driven in sync.
The app calls the green channel "blue" because R2-D2 is blue. We expose:
  - a "Blue" light  (green channel, brightness 0-3 scaled to 0-255 for HA)
  - a "Red" light   (red channel)
"""

from __future__ import annotations

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ColorMode,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_MAC, DOMAIN, LED_MAX
from .coordinator import R2D2Coordinator

# Map HA 0-255 brightness to device 0-3 and back
_HA_MAX = 255


def _ha_to_device(value: int) -> int:
    return max(0, min(LED_MAX, round(value * LED_MAX / _HA_MAX)))


def _device_to_ha(value: int) -> int:
    return round(value * _HA_MAX / LED_MAX)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: R2D2Coordinator = hass.data[DOMAIN][entry.entry_id]
    mac = entry.data[CONF_MAC]
    async_add_entities(
        [
            R2D2Light(coordinator, entry, mac, channel="blue"),
            R2D2Light(coordinator, entry, mac, channel="red"),
        ]
    )


class R2D2Light(LightEntity):
    """Single-channel brightness light for one R2D2 LED colour."""

    _attr_has_entity_name = True
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}

    def __init__(
        self,
        coordinator: R2D2Coordinator,
        entry: ConfigEntry,
        mac: str,
        channel: str,
    ) -> None:
        self._coordinator = coordinator
        self._channel = channel
        self._attr_unique_id = f"{mac}_led_{channel}"
        self._attr_name = f"LED {channel.capitalize()}"
        self._attr_icon = "mdi:led-on" if channel == "blue" else "mdi:led-variant-on"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, mac)},
            "name": entry.title,
            "manufacturer": "Clementoni",
            "model": "R2D2",
        }
        self._device_brightness: int = 0

    @property
    def is_on(self) -> bool:
        return self._device_brightness > 0

    @property
    def brightness(self) -> int:
        return _device_to_ha(self._device_brightness)

    async def async_turn_on(self, **kwargs) -> None:  # type: ignore[override]
        ha_brightness = kwargs.get(ATTR_BRIGHTNESS, _HA_MAX)
        device_val = _ha_to_device(ha_brightness)
        device_val = max(1, device_val)  # at least 1 when turning on
        await self._set(device_val)

    async def async_turn_off(self, **kwargs) -> None:  # type: ignore[override]
        await self._set(0)

    async def _set(self, device_val: int) -> None:
        self._device_brightness = device_val
        if self._channel == "blue":
            await self._coordinator.do_set_leds(blue=device_val)
        else:
            await self._coordinator.do_set_leds(red=device_val)
        self.async_write_ha_state()
