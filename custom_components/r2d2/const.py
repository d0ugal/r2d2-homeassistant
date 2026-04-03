"""Constants for the R2D2 integration."""

DOMAIN = "r2d2"
CONF_MAC = "mac_address"
DEFAULT_NAME = "R2D2"

# BLE
UUID_WRITE = "0000fff1-0000-1000-8000-00805f9b34fb"

# Packet structure
PACKET_HEADER = 0xB5
PACKET_FIXED_TAIL = bytes([0x7C, 0x6B, 0x5A, 0x49, 0x38, 0x27, 0x16, 0x05])

# Motor directions
MOTOR_STOP = 0x00
MOTOR_FORWARD = 0x01
MOTOR_REVERSE = 0x02
MOTOR_SPEED_DEFAULT = 0x03

# Head positions (byte value range 0x04–0x24)
HEAD_CENTER = 0x14
HEAD_LEFT = 0x04
HEAD_RIGHT = 0x24

HEAD_POSITIONS = {
    "left": HEAD_LEFT,
    "center": HEAD_CENTER,
    "right": HEAD_RIGHT,
}

# Sound IDs
SOUNDS = {
    "sound_1": 0x0A,
    "sound_2": 0x08,
    "sound_3": 0x09,
    "sound_4": 0x05,
}

# LED brightness: 0x00 (off) – 0x03 (max)
LED_OFF = 0x00
LED_MAX = 0x03
