from PIL import Image, ImageDraw, ImageFont
import os

import constants


# ========================= FONT HANDLING ================================

def load_led_font(size_label, font_path=None):
    """Loads Sans Serif font and maps size label → pixel size."""
    if size_label == "small":
        size = 8        # two-line capable
    elif size_label == "medium":
        size = 12       # single line
    elif size_label == "full":
        size = 15       # max height
    else:
        raise ValueError("Font size must be: small / medium / full")

    candidates = [
        font_path,
        r"fonts\arial.ttf",
        r"fonts\arialbd.ttf",
        r"fonts\verdana.ttf",
        r"fonts\SansSerifCollection.ttf"
    ]

    for c in candidates:
        if not c:
            continue
        try:
            return ImageFont.truetype(c, size)
        except:
            pass

    return ImageFont.load_default()


# ========================= TEXT RENDERING ===============================

def render_text_to_strip(text, font, color, multiline):
    """
    Renders full text into one long 16-pixel tall strip.
    multiline=True → two lines using 8px height each.
    """

    # compute bounding box width of whole text
    dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bbox = dummy.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]

    if multiline:
        # naive split
        split_index = len(text) // 2
        line1 = text[:split_index]
        line2 = text[split_index:]

        bbox1 = dummy.textbbox((0, 0), line1, font=font)
        bbox2 = dummy.textbbox((0, 0), line2, font=font)

        w = max(bbox1[2] - bbox1[0], bbox2[2] - bbox2[0])
        total_height = constants.IMG_H
    else:
        line1 = text
        line2 = ""
        total_height = constants.IMG_H

    # create full strip
    strip = Image.new("RGB", (w, total_height), (0, 0, 0))
    mask = Image.new("1", (w, total_height), 0)
    draw_mask = ImageDraw.Draw(mask)

    # -------- FIRST LINE (BOTTOM-ALIGNED) --------
    if line1:
        bbox1 = dummy.textbbox((0, 0), line1, font=font)
        glyph_h1 = bbox1[3] - bbox1[1]

        # bottom alignment for first (single) line
        y_bottom_1 = constants.IMG_H - glyph_h1
        base_y1 = y_bottom_1 - bbox1[1]

        draw_mask.text((0 - bbox1[0], base_y1), line1, font=font, fill=1)

    # -------- SECOND LINE (BOTTOM-ALIGNED IN LOWER HALF) --------
    if multiline and line2:
        bbox2 = dummy.textbbox((0, 0), line2, font=font)
        glyph_h2 = bbox2[3] - bbox2[1]

        # second line must sit in pixels 8–15 (lower half)
        y_bottom_2 = constants.IMG_H - glyph_h2
        # but do not overlap upper line → force ≥ 8px
        if y_bottom_2 < 8:
            y_bottom_2 = 8

        base_y2 = y_bottom_2 - bbox2[1]

        draw_mask.text((0 - bbox2[0], base_y2), line2, font=font, fill=1)

    # paste colored text
    strip.paste(color, mask=mask)
    return strip



# ========================= FRAME CUTTING ===============================

def split_strip_into_frames(strip):
    """Cuts long strip into 16×128 frames."""
    frames = []
    W = strip.width
    num_frames = (W + constants.IMG_W - 1) // constants.IMG_W  # ceil

    for i in range(num_frames):
        frame = Image.new("RGB", (constants.IMG_W, constants.IMG_H), (0, 0, 0))
        x0 = i * constants.IMG_W
        crop = strip.crop((x0, 0, x0 + constants.IMG_W, constants.IMG_H))
        frame.paste(crop, (0, 0))
        frames.append(frame)

    return frames


# ========================= MATRIX CONVERSION ===========================

def image_to_led_matrices(img):
    red = [[0] * constants.IMG_W for _ in range(constants.IMG_H)]
    green = [[0] * constants.IMG_W for _ in range(constants.IMG_H)]
    px = img.load()

    for y in range(constants.IMG_H):
        for x in range(constants.IMG_W):
            r, g, _ = px[x, y]
            red[y][x] = 1 if r > 0 else 0
            green[y][x] = 1 if g > 0 else 0

    return red, green


# ========================= MAIN ENTRY =================================

def generate_led_frames(text, size_label, color_name, font_path=None):
    """
    size_label = "small" / "medium" / "full"
    color_name = "red" / "green" / "yellow"
    """

    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "yellow": (255, 255, 0),
    }
    if color_name not in colors:
        raise ValueError("Color must be red/green/yellow")

    color = colors[color_name]

    font = load_led_font(size_label, font_path)
    multiline = (size_label == "small")

    strip = render_text_to_strip(text, font, color, multiline)

    frames = []
    for img in split_strip_into_frames(strip):
        frames.append(image_to_led_matrices(img))

    return frames


def save_red_channel_bitmaps(frames, output_dir="led_bitmaps"):
    """
    Saves each frame's RED matrix as a 16×128 BMP image.
    frames = list of (red_matrix, green_matrix)
    """
    os.makedirs(output_dir, exist_ok=True)

    for idx, (red, _) in enumerate(frames):
        img = Image.new("RGB", (constants.IMG_W, 16), (0, 0, 0))
        px = img.load()

        for y in range(constants.IMG_H):
            for x in range(constants.IMG_W):
                if red[y][x] == 1:
                    px[x, y] = (255, 0, 0)   # red pixel
                else:
                    px[x, y] = (0, 0, 0)     # black

        img.save(os.path.join(output_dir, f"frame_{idx:03d}.bmp"))