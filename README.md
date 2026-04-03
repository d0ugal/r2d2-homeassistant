# R2D2 Home Assistant Integration

A Home Assistant integration for the **Clementoni R2D2** remote-control droid. Connects
directly to the droid via Bluetooth with no cloud dependencies.

---

## Features

- **Move** — drive forward, reverse, left, or right for a set duration; stops automatically
- **Sound effects** — trigger any of R2D2's four built-in sound effects
- **Head control** — rotate the head to left, centre, or right
- **LED control** — set the blue and red LED brightness independently (0–3)
- **Automation-friendly** — all controls are service calls; combine them in any sequence

---

## Installation

Copy `custom_components/r2d2/` into your HA `config/custom_components/` directory and
restart Home Assistant. The droid will be discovered automatically via Bluetooth when
nearby, or add it manually via **Settings → Integrations → Add Integration → R2D2**.

---

## Services

### `r2d2.move`

Drive R2D2 in a direction for a set number of seconds. Stops automatically when the
duration expires, or immediately if `r2d2.stop` is called.

```yaml
action: r2d2.move
data:
  direction: forward   # forward | reverse | left | right
  move_for: 2          # seconds
  speed: 3             # optional, 0–3, default 3
```

### `r2d2.stop`

Stop all motors immediately, cancelling any in-progress move.

```yaml
action: r2d2.stop
```

### `r2d2.play_sound`

Play one of R2D2's built-in sound effects.

```yaml
action: r2d2.play_sound
data:
  sound: sound_1   # sound_1 | sound_2 | sound_3 | sound_4
```

### `r2d2.set_head`

Rotate R2D2's head to a preset position.

```yaml
action: r2d2.set_head
data:
  position: center   # left | center | right
```

### `r2d2.set_leds`

Set the brightness of the blue and/or red LEDs. 0 = off, 3 = maximum.

```yaml
action: r2d2.set_leds
data:
  blue: 3
  red: 0
```

---

## Example automations

**Greet someone at the door**
```yaml
automation:
  - alias: R2D2 Doorbell
    trigger:
      - platform: state
        entity_id: binary_sensor.front_door_visitor
        to: "on"
    action:
      - action: r2d2.play_sound
        data:
          sound: sound_1
      - delay: 2
      - action: r2d2.move
        data:
          direction: forward
          move_for: 1
```

**Scheduled wake-up**
```yaml
automation:
  - alias: R2D2 Morning
    trigger:
      - platform: time
        at: "08:00:00"
    action:
      - action: r2d2.set_leds
        data:
          blue: 3
      - action: r2d2.play_sound
        data:
          sound: sound_2
```

---

## Credits

The BLE protocol used by this integration was reverse-engineered and documented by
[PaulFinch/R2D2_Remote](https://github.com/PaulFinch/R2D2_Remote). Hat tip for doing
the hard work of figuring out the packet structure.
