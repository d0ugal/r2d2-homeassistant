# R2D2 Home Assistant Integration

A Home Assistant integration for the **Clementoni R2D2** remote-control droid. Connects
directly to the droid via Bluetooth with no cloud dependencies.

---

## Features

- **Move** — drive in 8 directions (cardinal + diagonal) for a set duration; stops automatically
- **Sound effects** — 10 built-in sound effects (sfx_1 through sfx_10)
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

Play one of R2D2's 10 built-in sound effects.

```yaml
action: r2d2.play_sound
data:
  sound: sfx_7   # sfx_1 through sfx_10
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
Both fields are optional — omitting one leaves it unchanged.

```yaml
action: r2d2.set_leds
data:
  blue: 3
  red: 0
```

---

## Example automations

**Drive forward and come back**

A simple script that moves forward, spins 180°, and returns.

```yaml
script:
  r2d2_there_and_back:
    alias: R2D2 There and Back
    sequence:
      - action: r2d2.play_sound
        data: {sound: sfx_7}
      - action: r2d2.move
        data: {direction: forward, move_for: 1.5, speed: 3}
      - delay: "00:00:01.7"
      - action: r2d2.move
        data: {direction: left, move_for: 0.7, speed: 3}
      - delay: "00:00:00.9"
      - action: r2d2.move
        data: {direction: forward, move_for: 1.5, speed: 3}
      - delay: "00:00:01.7"
      - action: r2d2.stop
```

**Flash lights and beep when a script finishes**

Useful as a notification at the end of any other automation.

```yaml
    action:
      - action: r2d2.set_leds
        data: {blue: 3, red: 0}
      - action: r2d2.play_sound
        data: {sound: sfx_7}
      - delay: "00:00:01"
      - action: r2d2.set_leds
        data: {blue: 0, red: 0}
```

**Spin and beep on button press**

Pair with an HA dashboard button or a physical Zigbee button.

```yaml
automation:
  - alias: R2D2 Button Press
    trigger:
      - platform: state
        entity_id: input_button.r2d2_spin
    action:
      - action: r2d2.set_leds
        data: {blue: 3, red: 0}
      - action: r2d2.play_sound
        data: {sound: sfx_7}
      - action: r2d2.move
        data: {direction: left, move_for: 0.8, speed: 3}
      - delay: "00:00:01"
      - action: r2d2.set_leds
        data: {blue: 0, red: 0}
      - action: r2d2.stop
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
