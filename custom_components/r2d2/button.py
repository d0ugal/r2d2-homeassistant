"""Button platform for R2D2 — momentary movement and sound actions."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from typing import Any

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_MAC, DOMAIN, SOUNDS
from .coordinator import R2D2Coordinator

_MOVE_DURATION = 0.5  # seconds for each movement button press

_SOUND_NAMES = {
    "sfx_1": "C-3PO",
    "sfx_2": "Chewbacca",
    "sfx_3": "Han Solo",
    "sfx_4": "Princess Leia",
    "sfx_5": "Luke Skywalker",
    "sfx_6": "Obi-Wan Kenobi",
    "sfx_7": "R2-D2",
    "sfx_8": "Stormtrooper",
    "sfx_9": "Darth Vader",
    "sfx_10": "Yoda",
}


@dataclass(frozen=True)
class R2D2ButtonDescription(ButtonEntityDescription):
    action: Callable[[R2D2Coordinator], Coroutine[Any, Any, None]] | None = None


_MOVEMENT_BUTTONS: list[R2D2ButtonDescription] = [
    R2D2ButtonDescription(
        key="move_forward",
        name="Move Forward",
        icon="mdi:arrow-up",
        action=lambda c: c.do_move("forward", _MOVE_DURATION),
    ),
    R2D2ButtonDescription(
        key="move_reverse",
        name="Move Reverse",
        icon="mdi:arrow-down",
        action=lambda c: c.do_move("reverse", _MOVE_DURATION),
    ),
    R2D2ButtonDescription(
        key="move_left",
        name="Turn Left",
        icon="mdi:arrow-left",
        action=lambda c: c.do_move("left", _MOVE_DURATION),
    ),
    R2D2ButtonDescription(
        key="move_right",
        name="Turn Right",
        icon="mdi:arrow-right",
        action=lambda c: c.do_move("right", _MOVE_DURATION),
    ),
    R2D2ButtonDescription(
        key="stop",
        name="Stop",
        icon="mdi:stop",
        action=lambda c: c.do_stop(),
    ),
]

_SOUND_BUTTONS: list[R2D2ButtonDescription] = [
    R2D2ButtonDescription(
        key=f"sound_{key}",
        name=f"Sound: {label}",
        icon="mdi:volume-high",
        action=lambda c, k=key: c.do_play_sound(k),
    )
    for key, label in _SOUND_NAMES.items()
    if key in SOUNDS
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: R2D2Coordinator = hass.data[DOMAIN][entry.entry_id]
    mac = entry.data[CONF_MAC]
    entities = [
        R2D2Button(coordinator, entry, mac, desc) for desc in _MOVEMENT_BUTTONS + _SOUND_BUTTONS
    ]
    async_add_entities(entities)


class R2D2Button(ButtonEntity):
    """A momentary button that fires a single R2D2 action."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: R2D2Coordinator,
        entry: ConfigEntry,
        mac: str,
        description: R2D2ButtonDescription,
    ) -> None:
        self._coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{mac}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, mac)},
            "name": entry.title,
            "manufacturer": "Clementoni",
            "model": "R2D2",
        }

    async def async_press(self) -> None:
        if self.entity_description.action:
            await self.entity_description.action(self._coordinator)
