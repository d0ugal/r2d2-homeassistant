# R2D2 Home Assistant Integration

A Home Assistant integration for the **Clementoni R2D2** remote-control droid. Connects
directly to the droid via Bluetooth with no cloud dependencies.

---

## Features

- **Move** — drive in 8 directions (cardinal + diagonal) for a set duration; stops automatically
- **Sound effects** — 16 character reaction sounds (8 Star Wars characters × good/bad reaction)
- **Head control** — rotate the head to left, centre, or right
- **LED control** — set the blue and red LED brightness independently (0–3)
- **BLE sensor** — exposes a `sensor.r2d2_ble_connected` entity showing connection state
- **Auto-discovery** — the droid is found automatically via Bluetooth when nearby
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
                       # forward_left | forward_right | reverse_left | reverse_right
  move_for: 2          # seconds (0.1–30)
  speed: 3             # optional, 0–3, default 3
```

Diagonal directions (e.g. `forward_left`) stop one motor and run the other so the
droid curves rather than spinning in place.

### `r2d2.stop`

Stop all motors immediately, cancelling any in-progress move.

```yaml
action: r2d2.stop
```

### `r2d2.play_sound`

Play one of R2D2's built-in character reaction sounds, discovered by disassembling
the official Android app.

```yaml
action: r2d2.play_sound
data:
  sound: r2d2_good
```

Available sounds:

| Sound key | Character | Reaction |
|---|---|---|
| `c3po_good` / `c3po_bad` | C-3PO | Good / Bad |
| `chewbacca_good` / `chewbacca_bad` | Chewbacca | Good / Bad |
| `han_good` / `han_bad` | Han Solo | Good / Bad |
| `leia_good` / `leia_bad` | Princess Leia | Good / Bad |
| `luke_good` / `luke_bad` | Luke Skywalker | Good / Bad |
| `obiwan_good` / `obiwan_bad` | Obi-Wan Kenobi | Good / Bad |
| `r2d2_good` / `r2d2_bad` | R2-D2 | Good / Bad |
| `stormtrooper_good` / `stormtrooper_bad` | Stormtrooper | Good / Bad |

### `r2d2.set_head`

Rotate R2D2's head to a preset position.

```yaml
action: r2d2.set_head
data:
  position: center   # left | center | right
```

### `r2d2.set_leds`

Set the brightness of the blue and/or red LEDs. 0 = off, 3 = maximum.
Both fields are optional — omitting one leaves it unchanged.

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
          sound: r2d2_good
      - delay: "00:00:02"
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
          sound: luke_good
```

---

## BLE protocol notes

The droid communicates over a single 20-byte write to UUID
`0000fff1-0000-1000-8000-00805f9b34fb`. The packet layout (confirmed by ARM64
disassembly of the official app's `libil2cpp.so`) is:

```
[0]    0xB5  header
[1]    sound ID
[2]    0x00
[3]    motor-1 direction  (0=stop, 1=fwd, 2=rev)
[4]    motor-1 speed      (0–3)
[5]    motor-2 direction
[6]    motor-2 speed
[7]    head position      (0x04=left, 0x14=centre, 0x24=right)
[8]    LED blue/green     (first unit, 0–3)
[9]    LED red            (first unit, 0–3)
[10]   LED blue/green     (second unit, mirror of [8])
[11]   LED red            (second unit, mirror of [9])
[12–19] fixed tail: 7C 6B 5A 49 38 27 16 05
```

The hardware has two bicolour (red/green) LED units. The app labels the green
channel "blue" because R2-D2 is blue.

---

## Credits

The BLE protocol was originally documented by
[PaulFinch/R2D2_Remote](https://github.com/PaulFinch/R2D2_Remote). The sound IDs
and full packet layout were further confirmed by disassembling the official
Clementoni Android app.
