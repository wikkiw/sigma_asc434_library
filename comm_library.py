from datetime import datetime
import re
import constants


# HELPERS


def matrix_IMG_HxIMG_W_to_bytes(matrix):
    """
    Convert a 16×128 binary matrix into 512 bytes.
    Each 4 bits becomes: 0011xxxx
    """
    out = bytearray()

    for row in matrix:
        for i in range(0, constants.IMG_W, 4):
            nib = 0
            for b in row[i:i+4]:
                nib = (nib << 1) | (b & 1)
            out.append((0b0011 << 4) | nib)

    return bytes(out)  # 512 bytes


def lcd_array_to_bytes(img_red, img_green):
    return matrix_IMG_HxIMG_W_to_bytes(img_red) + matrix_IMG_HxIMG_W_to_bytes(img_green)


# COMMANDS
def commands_set_text(text: str) -> list:
    """
    Build a text command:
        WRITE_START + WRITE_TEXT +
        (encoded text with {time}/{date}, colors, font changes)
        + WRITE_END
    Followed by CONFIRMATION.
    """

    # mapping of tokens → byte sequences
    token_map = {
        # time/date
        "{time}": constants.SHOW_TIME,
        "{date}": constants.SHOW_DATE,

        # colors
        "{color_red}": constants.COLOR_RED,
        "{color_green}": constants.COLOR_GREEN,
        "{color_yellow}": constants.COLOR_YELLOW,
        "{color_rg}": constants.COLOR_RED_GREEN,
        "{color_gr}": constants.COLOR_GREEN_RED,
        "{color_rainbow1}": constants.COLOR_RAINBOW1,
        "{color_rainbow2}": constants.COLOR_RAINBOW2,
        "{color_mix}": constants.COLOR_MIX,

        # fonts
        "{font_sserif7}": constants.FONT_SSERIF7,
        "{font_serif7}": constants.FONT_SERIF7,
        "{font_serif12}": constants.FONT_SERIF12,
        "{font_serif16}": constants.FONT_SERIF16,

        # actions
        "{action_none}": constants.ACTION_NONE,
        "{action_flash}": constants.ACTION_FLASH,
        "{action_flasht}": constants.ACTION_FLASH_TOP,
        "{action_flashb}": constants.ACTION_FLASH_BOTTOM,
        "{action_hold}": constants.ACTION_HOLD,
        "{action_holdt}": constants.ACTION_HOLD_TOP,
        "{action_holdb}": constants.ACTION_HOLD_BOTTOM,
        "{action_interlock}": constants.ACTION_INTERLOCK,
        "{action_shutter}": constants.ACTION_SHUTTER,

        # wait
        "{wait_0s}": constants.WAIT_0S,
        "{wait_1s}": constants.WAIT_1S,
        "{wait_2s}": constants.WAIT_2S,
        "{wait_3s}": constants.WAIT_3S,
        "{wait_4s}": constants.WAIT_4S,
        "{wait_5s}": constants.WAIT_5S,


        # settings
        "{next_frame}": constants.NEXT_FRAME,
    }

    # regex matching any token name
    pattern = re.compile(
        "(" + "|".join(re.escape(t) for t in token_map.keys()) + ")"
    )

    # Split text into token or plain segments
    parts = []
    idx = 0

    for match in pattern.finditer(text):
        start, end = match.span()

        # plain text before token
        if start > idx:
            parts.append(("text", text[idx:start]))

        # the token
        parts.append(("token", match.group(1)))

        idx = end

    # trailing plain text
    if idx < len(text):
        parts.append(("text", text[idx:]))

    # --- Construct the binary payload ---
    data = bytearray()

    data += constants.WRITE_START
    data += constants.WRITE_TEXT

    for kind, value in parts:
        if kind == "token":
            data += token_map[value]

        else:  # plain ASCII → hex
            hex_string = " ".join(f"{ord(c):02x}" for c in value)
            data += bytes.fromhex(hex_string)

    data += constants.WRITE_END

    return [
        bytes(data),
        constants.CONFIRMATION
    ]


def commands_show_custom_imgs(imgs):
    """
    Return list of PACKETS (bytes) ready to send.
    Each packet is bytes: ASCII header + binary frame + ASCII footer.
    """
    lead_in = bytes.fromhex("5d 21 5a 30 30 5d 22 41 5a 5d 3b 20 67")
    iter_start = bytes.fromhex("5d 3f 50")
    lead_out = bytes.fromhex("5d 24 5d 24")
    footer = constants.CONFIRMATION

    img_lead_in = bytes.fromhex("2e 5d 21 5a 30 30 5d 22 53")
    if constants.IMG_W == 128:
        img_lead_in_end = bytes.fromhex("32 40")
    else:
        img_lead_in_end = bytes.fromhex("32 50")

    commands = []

    # ---------- BUILD HEADER (ASCII ONLY) ----------
    header = bytearray()
    header.extend(lead_in)

    iterator = 97
    for i in range(len(imgs)):
        header.extend(iter_start)
        header.append(iterator)   # raw character 'a', 'b', 'c'
        if i < len(imgs)-1:
            #header.extend(b"])")
            header.extend(bytes.fromhex("5d 29"))
        iterator += 1

    header.extend(lead_out)
    commands.append(bytes(header))

    # ---------- BUILD IMAGE PACKETS ----------
    iterator = 97
    for img in imgs:
        red, green = img
        frame_bytes = lcd_array_to_bytes(red, green)  # 1024 raw bytes!

        packet = bytearray()
        packet.extend(img_lead_in)
        packet.append(iterator)
        packet.extend(img_lead_in_end)
        packet.extend(frame_bytes)    # *** RAW BYTES ***
        packet.extend(lead_out)

        commands.append(bytes(packet))
        iterator += 1

    # ---------- FINAL FOOTER ----------
    commands.append(footer)

    return commands


def commands_set_time_and_date(time: str = None, date: str = None) -> list:
    now = datetime.now()
    hhmm = now.strftime("%H%M%S")
    mmddyy = now.strftime("%m%d%y")

    if time is None:
        time = hhmm
    if date is None:
        date = mmddyy

    # Convert dynamic ASCII text into hex bytes
    def to_hex_bytes(text: str) -> bytes:
        return bytes.fromhex(" ".join(f"{ord(c):02X}" for c in text))

    # Static command prefixes/suffixes in hex
    prefix = bytes.fromhex("5d 21 5a 30 30 5d 22 45")   # ]!Z00]"E
    suffix = constants.WRITE_END               # ]$]$

    # DATE: ]!Z00]"E;MMDDYY]$]$
    date_part = prefix + bytes.fromhex("3b") + to_hex_bytes(date) + suffix

    # TIME: ]!Z00]"E HHMM]$]$
    time_part = prefix + bytes.fromhex("20") + to_hex_bytes(time) + suffix

    commands = [
        date_part,
        constants.CONFIRMATION,
        time_part,
        constants.CONFIRMATION
    ]

    return commands


def commands_set_width(width: int = 128) -> list:

    if width not in [128, 256]:
        raise ValueError("Supported widths are 128 and 256px")

    cmd_128 = bytes.fromhex("5d 21 5a 30 30 5d 22 59 39 10 10 00 5d 24")
    cmd_256 = bytes.fromhex("5d 21 5a 30 30 5d 22 59 39 10 20 00 5d 24")

    if width == 128:
        return [cmd_128]
    else:
        return [cmd_256]


def commands_clear_memory():

    cmd = bytes.fromhex("5d 21 5a 30 30 5d 22 58 5d 24")

    return [cmd]
