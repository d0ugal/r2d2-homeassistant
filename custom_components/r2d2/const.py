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

# Sound IDs (GoodRobotReaction / BadRobotReaction pairs per character,
# discovered by disassembling the Clementoni Android APK)
SOUNDS = {
    # C-3PO
    "c3po_good": 0x08,
    "c3po_bad": 0x07,
    # Chewbacca
    "chewbacca_good": 0x09,
    "chewbacca_bad": 0x06,
    # Han Solo
    "han_good": 0x0A,
    "han_bad": 0x05,
    # Princess Leia
    "leia_good": 0x0B,
    "leia_bad": 0x04,
    # Luke Skywalker
    "luke_good": 0x0C,
    "luke_bad": 0x03,
    # Obi-Wan Kenobi
    "obiwan_good": 0x0D,
    "obiwan_bad": 0x02,
    # R2-D2
    "r2d2_good": 0x0E,
    "r2d2_bad": 0x01,
    # Stormtrooper
    "stormtrooper_good": 0x0F,
    "stormtrooper_bad": 0x00,
}

# Additional sounds found in APK not mapped to a character reaction
# (snd byte, byte[3]=0x00 normal mode — purpose unknown, for testing)
SOUNDS_EXTRA = {
    "extra_0x0b": 0x0B,
    "extra_0x18": 0x18,
    "extra_0x1e": 0x1E,
    "extra_0x1f": 0x1F,
    "extra_0x20": 0x20,
}

# Animation/sequence trigger packets (byte[3]=0x06, all motor bytes 0x00)
# Found in APK — exact behaviour unknown, for future testing.
# Values are the snd byte (byte[1]).
ANIMATIONS = {
    "anim_0x00": 0x00,
    "anim_0x02": 0x02,
    "anim_0x03": 0x03,
    "anim_0x04": 0x04,
    "anim_0x05": 0x05,
    "anim_0x06": 0x06,
    "anim_0x07": 0x07,
    "anim_0x08": 0x08,
    "anim_0x09": 0x09,
    "anim_0x0c": 0x0C,
    "anim_0x0d": 0x0D,
    "anim_0x0f": 0x0F,
    "anim_0x13": 0x13,
    "anim_0x15": 0x15,
    "anim_0x1c": 0x1C,
    "anim_0x28": 0x28,
}

# LED brightness: 0x00 (off) – 0x03 (max)
LED_OFF = 0x00
LED_MAX = 0x03
