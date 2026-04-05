"""Select platform for R2D2 — head position."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_MAC, DOMAIN
from .coordinator import R2D2Coordinator

_HEAD_OPTIONS = ["left", "center", "right"]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: R2D2Coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([R2D2HeadSelect(coordinator, entry)])


class R2D2HeadSelect(SelectEntity):
    """Select entity to control R2D2's head position."""

    _attr_has_entity_name = True
    _attr_name = "Head Position"
    _attr_icon = "mdi:rotate-360"
    _attr_options = _HEAD_OPTIONS

    def __init__(self, coordinator: R2D2Coordinator, entry: ConfigEntry) -> None:
        self._coordinator = coordinator
        mac = entry.data[CONF_MAC]
        self._attr_unique_id = f"{mac}_head_position"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, mac)},
            "name": entry.title,
            "manufacturer": "Clementoni",
            "model": "R2D2",
        }
        self._attr_current_option = "center"

    async def async_select_option(self, option: str) -> None:
        await self._coordinator.do_set_head(option)
        self._attr_current_option = option
        self.async_write_ha_state()
