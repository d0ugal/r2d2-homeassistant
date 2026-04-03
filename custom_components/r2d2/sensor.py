"""Sensor platform for R2D2 — BLE connectivity."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_MAC, DOMAIN
from .coordinator import R2D2Coordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: R2D2Coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([R2D2BLESensor(coordinator, entry)])


class R2D2BLESensor(CoordinatorEntity[R2D2Coordinator], SensorEntity):
    """Shows whether the BLE link to R2D2 is currently active."""

    _attr_has_entity_name = True
    _attr_name = "BLE Connected"

    def __init__(self, coordinator: R2D2Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        mac = entry.data[CONF_MAC]
        self._attr_unique_id = f"{mac}_ble_connected"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, mac)},
            "name": entry.title,
            "manufacturer": "Clementoni",
            "model": "R2D2",
        }

    @property
    def native_value(self) -> str:
        connected = (self.coordinator.data or {}).get("connected", False)
        return "connected" if connected else "disconnected"
