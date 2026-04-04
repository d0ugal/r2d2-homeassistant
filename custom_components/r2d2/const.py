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

# The 10 direct sound IDs confirmed from the Sfx1–Sfx10 table in libil2cpp.so.
# Cross-referenced with the character reaction table to give meaningful names.
# The app's character gallery triggers full movement+sound sequences; these are
# just the raw sound bytes used by the numbered sound UI.
SOUNDS = {
    "sfx_1":  0x01,  # R2-D2
    "sfx_2":  0x02,  # Obi-Wan Kenobi
    "sfx_3":  0x03,  # Luke Skywalker
    "sfx_4":  0x04,  # Princess Leia
    "sfx_5":  0x05,  # Han Solo
    "sfx_6":  0x06,  # Chewbacca
    "sfx_7":  0x07,  # C-3PO
    "sfx_8":  0x08,  # C-3PO (alternate)
    "sfx_9":  0x0A,  # Han Solo (alternate)
    "sfx_10": 0x0C,  # Luke Skywalker (alternate)
}

# Character reaction byte pairs (GoodRobotReaction / BadRobotReaction).
# These are NOT just sounds — the official app combines them with movement
# sequences. Kept here for reference/experimentation.
# NOTE: 0x00 (stormtrooper_bad) = silence; 0x09/0x0B/0x0D–0x0F are reaction
# bytes not present in the Sfx table and may duplicate nearby sounds.
CHARACTER_SOUNDS = {
    "r2d2_bad":          0x01,
    "obiwan_bad":        0x02,
    "luke_bad":          0x03,
    "leia_bad":          0x04,
    "han_bad":           0x05,
    "chewbacca_bad":     0x06,
    "c3po_bad":          0x07,
    "c3po_good":         0x08,
    "chewbacca_good":    0x09,
    "han_good":          0x0A,
    "leia_good":         0x0B,
    "luke_good":         0x0C,
    "obiwan_good":       0x0D,
    "r2d2_good":         0x0E,
    "stormtrooper_good": 0x0F,
    "stormtrooper_bad":  0x00,  # silence
}

# Additional sounds found in APK (purpose unknown, for testing)
SOUNDS_EXTRA = {
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
