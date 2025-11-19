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

# Wait
WAIT_5S = bytes.fromhex("5d 35")
WAIT_4S = bytes.fromhex("5d 36")
WAIT_3S = bytes.fromhex("5d 37")
WAIT_2S = bytes.fromhex("5d 38")
WAIT_1S = bytes.fromhex("5d 39")
WAIT_0S = bytes.fromhex("5d 29")

# Settings
NEXT_FRAME = bytes.fromhex("5d 2c")


