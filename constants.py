IMG_W = 128
IMG_H = 16

# Communication

# Write confirmation
# .]!Z00]"E.  Z]$]$
CONFIRMATION = bytes.fromhex("2e 5d 21 5a 30 30 5d 22 45 2e 20 20 5a 5d 24 5d 24")

# Write start
# ]!Z00]"
WRITE_START = bytes.fromhex("5d 21 5a 30 30 5d 22")
# ]$]$
WRITE_END = bytes.fromhex("5d 24 5d 24")
# AZ
WRITE_TEXT = bytes.fromhex("41 5a")

# ]3
SHOW_TIME = bytes.fromhex("5d 33")
# ]+3
SHOW_DATE = bytes.fromhex("5d 2b 33")

# Colors
COLOR_RED = bytes.fromhex("5d 3c 31")
COLOR_GREEN = bytes.fromhex("5d 3c 32")
COLOR_RED_GREEN = bytes.fromhex("5d 3c 34")
COLOR_GREEN_RED = bytes.fromhex("5d 3c 35")
COLOR_YELLOW = bytes.fromhex("5d 3c 38")
COLOR_RAINBOW2 = bytes.fromhex("5d 3c 39")
COLOR_RAINBOW1 = bytes.fromhex("5d 3c 41")
COLOR_MIX = bytes.fromhex("5d 3c 42")

# Fonts
FONT_SSERIF7 = bytes.fromhex("5d 3a 41")
FONT_SERIF7 = bytes.fromhex("5d 3a 45")
FONT_SERIF12 = bytes.fromhex("5d 3a 4c")
FONT_SERIF16 = bytes.fromhex("5d 3a 47")

# Actions
ACTION_NONE = bytes.fromhex("5d 3b 20 61")
ACTION_FLASH = bytes.fromhex("5d 3b 20 63")
ACTION_FLASH_TOP = bytes.fromhex("5d 3b 22 63")
ACTION_FLASH_BOTTOM = bytes.fromhex("5d 3b 26 63")
ACTION_HOLD = bytes.fromhex("5d 3b 20 62")
ACTION_HOLD_TOP = bytes.fromhex("5d 3b 22 62")
ACTION_HOLD_BOTTOM = bytes.fromhex("5d 3b 26 62")
ACTION_INTERLOCK = bytes.fromhex("5d 3b 20 6e 33")
ACTION_SHUTTER = bytes.fromhex("5d 3b 20 64")
ACTION_ROLL_LEFT = bytes.fromhex("5d 3b 20 67")
ACTION_ROLL_LEFT_TOP = bytes.fromhex("5d 3b 22 67")
ACTION_ROLL_LEFT_BOTTOM = bytes.fromhex("5d 3b 26 67")
ACTION_ROLL_RIGHT = bytes.fromhex("5d 3b 20 68")
ACTION_ROLL_RIGHT_TOP = bytes.fromhex("5d 3b 22 68")
ACTION_ROLL_RIGHT_BOTTOM = bytes.fromhex("5d 3b 26 68")
ACTION_ROLL_UP = bytes.fromhex("5d 3b 20 65")
ACTION_ROLL_UP_TOP = bytes.fromhex("5d 3b 22 65")
ACTION_ROLL_UP_BOTTOM = bytes.fromhex("5d 3b 26 65")
ACTION_ROLL_DOWN = bytes.fromhex("5d 3b 20 66")
ACTION_ROLL_DOWN_TOP = bytes.fromhex("5d 3b 22 66")
ACTION_ROLL_DOWN_BOTTOM = bytes.fromhex("5d 3b 26 66")
ACTION_ROLL_IN = bytes.fromhex("5d 3b 20 70")
ACTION_ROLL_IN_TOP = bytes.fromhex("5d 3b 22 70")
ACTION_ROLL_IN_BOTTOM = bytes.fromhex("5d 3b 26 70")
ACTION_ROLL_OUT = bytes.fromhex("5d 3b 20 71")
ACTION_ROLL_OUT_TOP = bytes.fromhex("5d 3b 22 71")
ACTION_ROLL_OUT_BOTTOM = bytes.fromhex("5d 3b 26 71")

ACTION_ROTATE = bytes.fromhex("5d 3b 20 61")
ACTION_ROTATE_TOP = bytes.fromhex("5d 3b 22 61")
ACTION_ROTATE_BOTTOM = bytes.fromhex("5d 3b 26 61")
ACTION_SCROLL = bytes.fromhex("5d 3b 20 6d")
ACTION_SCROLL_TOP = bytes.fromhex("5d 3b 22 6d")
ACTION_SCROLL_BOTTOM = bytes.fromhex("5d 3b 26 6d")
ACTION_SLIDE = bytes.fromhex("5d 3b 20 6e 35")
ACTION_SLIDE_TOP = bytes.fromhex("5d 3b 22 6e 35")
ACTION_SLIDE_BOTTOM = bytes.fromhex("5d 3b 26 6e 35")
ACTION_SNOW = bytes.fromhex("5d 3b 20 6e 32")
ACTION_SNOW_TOP = bytes.fromhex("5d 3b 22 6e 32")
ACTION_SNOW_BOTTOM = bytes.fromhex("5d 3b 26 6e 32")
ACTION_SPARKLE = bytes.fromhex("5d 3b 20 6e 31")
ACTION_SPARKLE_TOP = bytes.fromhex("5d 3b 22 6e 31")
ACTION_SPARKLE_BOTTOM = bytes.fromhex("5d 3b 26 6e 31")
ACTION_SPRAY = bytes.fromhex("5d 3b 20 6e 36")
ACTION_SPRAY_TOP = bytes.fromhex("5d 3b 22 6e 36")
ACTION_SPRAY_BOTTOM = bytes.fromhex("5d 3b 26 6e 36")
ACTION_STARBURST = bytes.fromhex("5d 3b 20 6e 37")
ACTION_STARBURST_TOP = bytes.fromhex("5d 3b 22 6e 37")
ACTION_STARBURST_BOTTOM = bytes.fromhex("5d 3b 26 6e 37")
ACTION_SWITCH = bytes.fromhex("5d 3b 20 6e 34")
ACTION_SWITCH_TOP = bytes.fromhex("5d 3b 22 6e 34")
ACTION_SWITCH_BOTTOM = bytes.fromhex("5d 3b 26 6e 34")
ACTION_TWINKLE = bytes.fromhex("5d 3b 20 6e 30")
ACTION_TWINKLE_TOP = bytes.fromhex("5d 3b 22 6e 30")
ACTION_TWINKLE_BOTTOM = bytes.fromhex("5d 3b 26 6e 30")
ACTION_WIPE_LEFT = bytes.fromhex("5d 3b 20 6b")
ACTION_WIPE_LEFT_TOP = bytes.fromhex("5d 3b 22 6b")
ACTION_WIPE_LEFT_BOTTOM = bytes.fromhex("5d 3b 26 6b")
ACTION_WIPE_RIGHT = bytes.fromhex("5d 3b 20 6c")
ACTION_WIPE_RIGHT_TOP = bytes.fromhex("5d 3b 22 6c")
ACTION_WIPE_RIGHT_BOTTOM = bytes.fromhex("5d 3b 26 6c")
ACTION_WIPE_UP = bytes.fromhex("5d 3b 20 69")
ACTION_WIPE_UP_TOP = bytes.fromhex("5d 3b 22 69")
ACTION_WIPE_UP_BOTTOM = bytes.fromhex("5d 3b 26 69")
ACTION_WIPE_DOWN = bytes.fromhex("5d 3b 20 6a")
ACTION_WIPE_DOWN_TOP = bytes.fromhex("5d 3b 22 6a")
ACTION_WIPE_DOWN_BOTTOM = bytes.fromhex("5d 3b 26 6a")
ACTION_WIPE_IN = bytes.fromhex("5d 3b 20 73")
ACTION_WIPE_IN_TOP = bytes.fromhex("5d 3b 22 73")
ACTION_WIPE_IN_BOTTOM = bytes.fromhex("5d 3b 26 73")
ACTION_WIPE_OUT = bytes.fromhex("5d 3b 20 72")
ACTION_WIPE_OUT_TOP = bytes.fromhex("5d 3b 22 72")
ACTION_WIPE_OUT_BOTTOM = bytes.fromhex("5d 3b 26 72")
ACTION_WIPE_MIDDLE = bytes.fromhex("5d 3b 20 6e 38")
ACTION_WIPE_MIDDLE_TOP = bytes.fromhex("5d 3b 22 6e 38")
ACTION_WIPE_MIDDLE_BOTTOM = bytes.fromhex("5d 3b 26 6e 38")

# Wait
WAIT_5S = bytes.fromhex("5d 35")
WAIT_4S = bytes.fromhex("5d 36")
WAIT_3S = bytes.fromhex("5d 37")
WAIT_2S = bytes.fromhex("5d 38")
WAIT_1S = bytes.fromhex("5d 39")
WAIT_0S = bytes.fromhex("5d 29")

# Settings
NEXT_FRAME = bytes.fromhex("5d 2c")


