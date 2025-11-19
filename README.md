# Sigma LED Panel Library (ASC 434)

Python library and tools for controlling a Sigma / ASC 434 LED panel over a serial (COM) port.

The project contains:

- **Protocol constants** for the panel (raw hex commands).
- **High-level command builders** (set time/date, set width, clear memory, send text, send custom images).
- **Text → LED frame generator** using Pillow (supports Unicode, including Czech diacritics with suitable fonts).
- **CLI example** (`main.py`).
- **Tkinter GUI frontend** (`gui_frontend.py`) with buttons, token inserter, custom text and custom frames editor.
- **Serial port test tool** (`test_com_port.py`).

---

## Project structure

```text
sigma-library/
└── sigma-library/
    ├── comm_library.py        # High-level commands and protocol helpers
    ├── constants.py           # Panel constants and token→byte mappings
    ├── text_to_frames.py      # Text → PIL image → LED frame matrices (red/green)
    ├── main.py                # Example CLI usage / experiments
    ├── gui_frontend.py        # Tkinter GUI (frontend for the library) – add from this repo
    ├── test_com_port.py       # List & test serial ports
    ├── fonts/                 # Optional: TTF/OTF fonts for text rendering
    ├── test_bitmaps/          # Example exported bitmaps (debug/preview)
    ├── vystup/                # Output folder for generated bitmaps
    ├── venv/                  # Local virtualenv (not required, can be ignored/deleted)
    └── __pycache__/           # Python bytecode cache
````

> **Note:** The checked-in `venv/` is specific to the original machine. For a clean setup, it’s better to create your own virtual environment and ignore/remove this folder.

---

## Requirements

* Python **3.10+** (tested with 3.11)
* Packages:

  * [`pyserial`](https://pypi.org/project/pyserial/) – serial port communication
  * [`Pillow`](https://pypi.org/project/Pillow/) – text rendering to bitmaps

### Installation

From the inner `sigma-library/` folder:

```bash
cd sigma-library/sigma-library

# (Recommended) Create a fresh virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install pyserial Pillow
```

If you want a `requirements.txt`, it can simply contain:

```text
pyserial
Pillow
```

---

## Configuration

### Panel size

The panel is treated as a `IMG_H × IMG_W` matrix:

```python
# constants.py
IMG_W = 128
IMG_H = 16
```

Supported widths at the moment:

* `128`
* `256`

In the **GUI**, the **“Set width (and update IMG_W)”** button:

* sends the correct command to the panel,
* updates `constants.IMG_W` at runtime
* so that `generate_led_frames()` and all matrix conversions match the hardware width.

If you are using the **CLI only**, make sure `IMG_W` matches your panel width before generating frames.

### Serial port

In the GUI, the port and baudrate are editable at the top of the window.

* On **Windows**: `COM3`, `COM4`, …
* On **Linux**: `/dev/ttyUSB0`, `/dev/ttyACM0`, …

Use `test_com_port.py` to list and test available ports.

---

## Library overview

### `constants.py`

Defines:

* **Panel dimensions**: `IMG_W`, `IMG_H`
* Low-level command pieces (all as `bytes.fromhex`):

  * `WRITE_START`, `WRITE_TEXT`, `WRITE_END`, `CONFIRMATION`, …
* **Color commands**:

  * `COLOR_RED`, `COLOR_GREEN`, `COLOR_YELLOW`,
  * `COLOR_RED_GREEN`, `COLOR_GREEN_RED`,
  * `COLOR_RAINBOW1`, `COLOR_RAINBOW2`, `COLOR_MIX`.
* **Font commands**:

  * `FONT_SSERIF7`, `FONT_SERIF7`, `FONT_SERIF12`, `FONT_SERIF16`.
* **Actions**:

  * `ACTION_NONE`, `ACTION_FLASH`, `ACTION_FLASH_TOP`, `ACTION_FLASH_BOTTOM`,
  * `ACTION_HOLD`, `ACTION_HOLD_TOP`, `ACTION_HOLD_BOTTOM`,
  * `ACTION_INTERLOCK`, `ACTION_SHUTTER`.
* **Waits**:

  * `WAIT_0S`, `WAIT_1S`, `WAIT_2S`, `WAIT_3S`, `WAIT_4S`, `WAIT_5S`.
* **Other**:

  * `NEXT_FRAME` – go to next frame in stored text/animation.
* **Special placeholders**:

  * `SHOW_TIME`, `SHOW_DATE` – for inserting current time/date inside text.

These constants are used by `comm_library.py` and by the text token system.

---

### `comm_library.py`

Contains protocol helpers and high-level command builders.

Key functions:

* `matrix_IMG_HxIMG_W_to_bytes(matrix)`
  Converts a `IMG_H × IMG_W` binary matrix (0/1) into panel-specific bytes.
  Each group of 4 bits is encoded as `0011xxxx`.

* `lcd_array_to_bytes(frames)`
  Takes a list of `(red_matrix, green_matrix)` and converts them into bytes for the panel.

* `commands_set_text(text: str) -> list[bytes]`
  Builds a text command:

  * Prefix: `WRITE_START + WRITE_TEXT`
  * Parses **tokens** inside curly braces and replaces them with bytes from `constants`
  * Appends `WRITE_END`
  * Adds final `CONFIRMATION` command.

  Supported tokens include (non-exhaustive):

  * Time/date:

    * `{time}` → current time on panel (uses `SHOW_TIME`)
    * `{date}` → current date on panel (uses `SHOW_DATE`)
  * Colors:

    * `{color_red}`, `{color_green}`, `{color_yellow}`
    * `{color_rg}`, `{color_gr}`
    * `{color_rainbow1}`, `{color_rainbow2}`, `{color_mix}`
  * Fonts:

    * `{font_sserif7}`, `{font_serif7}`, `{font_serif12}`, `{font_serif16}`
  * Actions:

    * `{action_none}`, `{action_flash}`, `{action_flasht}`, `{action_flashb}`
    * `{action_hold}`, `{action_holdt}`, `{action_holdb}`
    * `{action_interlock}`, `{action_shutter}`
  * Wait times:

    * `{wait_0s}`, `{wait_1s}`, `{wait_2s}`, `{wait_3s}`, `{wait_4s}`, `{wait_5s}`
  * Other:

    * `{next_frame}` – split the text into multiple frames on the panel

  Example:

  ```python
  from comm_library import commands_set_text

  text = (
      "{action_holdt}{font_sserif7}{color_rg}"
      "EASE {color_yellow}- Effortless Algorithmic Solution Evolution "
      "{wait_3s}{next_frame}{color_red}Frame 2 with time: {time}"
  )

  commands = commands_set_text(text)
  ```

* `commands_show_custom_imgs(frames) -> list[bytes]`
  Turns a list of `(red, green)` matrices (as produced by `generate_led_frames`) into the full sequence of bytes to show these frames on the panel.

* `commands_set_time_and_date(time: str | None = None, date: str | None = None) -> list[bytes]`
  Builds commands to set the panel’s internal time and date:

  * If `time` / `date` are `None`, uses current system time.
  * Time format: `hhmm`
  * Date format: `mmddyy`

* `commands_set_width(width: int) -> list[bytes]`
  Returns the correct command for setting panel width:

  * `width == 128` → command for 16×128
  * `width == 256` → command for 16×256

* `commands_clear_memory() -> list[bytes]`
  Returns a command sequence to clear the panel’s internal memory.

All of these functions **only build byte sequences**. Sending is done in `main.py` and `gui_frontend.py`.

---

### `text_to_frames.py`

Responsible for converting arbitrary text (UTF-8, including diacritics) into LED frames.

Key parts:

* `load_led_font(size_label, font_path=None)`

  * `size_label`: `"small"`, `"medium"`, `"full"`
  * Maps to pixel sizes: 8 / 12 / 15.
  * Tries a list of candidate fonts:

    * `font_path` (if provided)
    * `fonts\arial.ttf`, `fonts\arialbd.ttf`, `fonts\verdana.ttf`, `fonts\SansSerifCollection.ttf`
  * Falls back to `ImageFont.load_default()` if all fail.

* `generate_led_frames(text, size_label, color_name, font_path=None)`
  High-level entry point:

  * Renders the full text into a large off-screen image (width ≥ panel width, height 16 px).
  * Splits it into consecutive frames of size `IMG_H × IMG_W`.
  * For each frame, converts it into:

    * `red` matrix (list of lists of 0/1)
    * `green` matrix
  * Returns: `List[Tuple[red_matrix, green_matrix]]`.

  Arguments:

  * `text`: arbitrary Unicode string (Czech diacritics supported if the font does).
  * `size_label`: `"small"`, `"medium"`, `"full"`.
  * `color_name`: `"red"`, `"green"`, `"yellow"` – controls color of rendered pixels.
  * `font_path`: optional TTF/OTF path; if not given, uses default candidates in `fonts/`.

* `image_to_led_matrices(img)`
  Converts a PIL `Image` into `(red, green)` matrices based on RGB channels.

* `save_red_channel_bitmaps(frames, output_dir="test_bitmaps")`
  Saves each frame’s red channel as a `frame_XXX.bmp` image for debugging.

---

## Tools

### `test_com_port.py`

Small helper for listing and testing serial ports.

```bash
python test_com_port.py
```

* Lists all available ports.
* Prompts for a port name (e.g. `COM4` / `/dev/ttyUSB0`).
* Sends some test data and reports whether the port is reachable.

---

## CLI usage (`main.py`)

`main.py` is an example script showing how to use the library from code.
Typical pattern:

1. Build commands via `comm_library`.
2. Open `serial.Serial`.
3. Send each command (bytes) to the panel.
4. Optionally read responses.

Example snippet:

```python
import serial
from comm_library import commands_set_text
import constants

def send_commands(commands):
    ser = serial.Serial(port="COM4", baudrate=9600, timeout=3)
    for cmd in commands:
        ser.write(cmd)
        ser.flush()
    ser.close()

if __name__ == "__main__":
    text = "{color_red}Hello world {time}{wait_3s}"
    commands = commands_set_text(text)
    send_commands(commands)
```

You can also use `generate_led_frames` + `commands_show_custom_imgs` for full-custom bitmaps:

```python
from comm_library import commands_show_custom_imgs
from text_to_frames import generate_led_frames

frames = generate_led_frames(
    text="Ahoj světe! Čau panel.",
    size_label="full",
    color_name="red",
    font_path=r"fonts\SansSerifCollection.ttf",  # optional
)

commands = commands_show_custom_imgs(frames)
send_commands(commands)
```

---

## GUI frontend (`gui_frontend.py`)

The GUI wraps the library into a simple, panel-oriented application.

Features:

* **Connection panel**

  * Select serial port (e.g. `COM4` / `/dev/ttyUSB0`).
  * Select baudrate (default `9600`).

* **Panel commands**

  * **Set current time & date** → `commands_set_time_and_date()`
  * **Set width (and update IMG_W)** → `commands_set_width(width)` + update `constants.IMG_W`
  * **Clear memory** → `commands_clear_memory()`

* **Text editor**

  * Free text area for `commands_set_text(text)`.
  * **Token buttons** that insert tokens at the cursor:

    * Time/date: `{time}`, `{date}`
    * Colors: `{color_red}`, `{color_green}`, `{color_yellow}`, `{color_rg}`, `{color_gr}`, `{color_rainbow1}`, `{color_rainbow2}`, `{color_mix}`
    * Fonts: `{font_sserif7}`, `{font_serif7}`, `{font_serif12}`, `{font_serif16}`
    * Actions: `{action_none}`, `{action_flash}`, `{action_flasht}`, `{action_flashb}`, `{action_hold}`, `{action_holdt}`, `{action_holdb}`, `{action_interlock}`, `{action_shutter}`
    * Waits: `{wait_0s}`–`{wait_5s}`
    * Other: `{next_frame}`
  * Button **“Send text to panel”**:

    * Builds commands via `commands_set_text`
    * Sends them over serial.

* **Custom frames (for diacritics / custom fonts)**

  * Input field for **UTF-8 text** (supports Czech diacritics).
  * Select **size**: `"small"`, `"medium"`, `"full"`.
  * Select **base color**: `"red"`, `"green"`, `"yellow"`.
  * Optional **font file** browser (TTF/OTF).
  * Button **“Generate frames and send to panel”**:

    * Calls `generate_led_frames(...)`
    * Builds commands via `commands_show_custom_imgs(frames)`
    * Sends them over serial.

* **Log window**

  * Shows all sent commands (hex), port info, and any responses from the panel.
  * Minimal height of the main window is set so the log is always visible.

### Running the GUI

From `sigma-library/sigma-library`:

```bash
python gui_frontend.py
```

Set the correct **COM port**, then try:

* **Set current time & date**
* Type text in the editor (e.g. with tokens) and hit **Send text to panel**
* Or type arbitrary UTF-8 text in the **Custom frames** section and send as images.

---

## Notes / Tips

* If you change the panel width manually or via another tool, make sure:

  * `constants.IMG_W` matches the actual panel,
  * or in the GUI you press **“Set width (and update IMG_W)”** to synchronize everything.
* For best diacritic support, use a TTF font that contains Czech glyphs and point `font_path` to it.
* The project is designed so that:

  * **`constants.py`** knows nothing about Pillow/serial.
  * **`comm_library.py`** knows only about bytes and protocol.
  * **`text_to_frames.py`** knows only about images and matrices.
  * **`main.py` / `gui_frontend.py`** glue everything together and talk to the serial port.

---

## License

No explicit license has been set yet.