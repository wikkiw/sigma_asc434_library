import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import scrolledtext
import time
import serial
import serial.tools.list_ports

import constants
from comm_library import (
    commands_set_text,
    commands_show_custom_imgs,
    commands_set_time_and_date,
    commands_set_width,
    commands_clear_memory,
)
from text_to_frames import generate_led_frames


class SigmaPanelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sigma / ASC Panel Controller")
        self.geometry("950x950")

        # --- connection settings ---
        self.port_var = tk.StringVar(value="COM4")   # change if needed
        self.baud_var = tk.StringVar(value="9600")

        self.ports = [p.device for p in serial.tools.list_ports.comports()]
        if self.ports:
            self.port_var.set(self.ports[0])

        # --- token groups for text editor ---
        # All tokens supported by commands_set_text
        self.token_groups = {
            "Time/Date": [
                "{time}",
                "{date}",
            ],
            "Colors": [
                "{color_red}",
                "{color_green}",
                "{color_yellow}",
                "{color_rg}",
                "{color_gr}",
                "{color_rainbow1}",
                "{color_rainbow2}",
                "{color_mix}",
            ],
            "Fonts": [
                "{font_sserif7}",
                "{font_serif7}",
                "{font_serif12}",
                "{font_serif16}",
            ],
            "Actions": [
                "{action_none}",
                "{action_flash}",
                "{action_flasht}",
                "{action_flashb}",
                "{action_hold}",
                "{action_holdt}",
                "{action_holdb}",
                "{action_interlock}",
                "{action_shutter}",
            ],
            "Wait": [
                "{wait_0s}",
                "{wait_1s}",
                "{wait_2s}",
                "{wait_3s}",
                "{wait_4s}",
                "{wait_5s}",
            ],
            "Other": [
                "{next_frame}",
            ],
        }

        self._build_connection_frame()
        self._build_control_frame()
        self._build_text_frame()
        self._build_custom_frames_frame()
        self._build_log_frame()

        self.after(100, lambda: self.log("Log inicializován, aplikace spuštěna.\n"))

    # ------------------------------------------------------------------ UI builders
    def _build_connection_frame(self):
        frame = ttk.LabelFrame(self, text="Connection")
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="Serial port:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame, textvariable=self.port_var, width=12).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Baudrate:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(frame, textvariable=self.baud_var, width=8).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame, text="(default 9600)").grid(row=0, column=4, padx=5, pady=5, sticky="w")

    def _build_control_frame(self):
        frame = ttk.LabelFrame(self, text="Panel commands")
        frame.pack(fill="x", padx=10, pady=5)

        # Set time & date
        ttk.Button(
            frame,
            text="Set current time & date",
            command=self.on_set_time_date,
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Width selector + button
        self.width_var = tk.IntVar(value=constants.IMG_W)
        ttk.Label(frame, text="Width:").grid(row=0, column=1, padx=5, pady=5, sticky="e")
        ttk.Radiobutton(frame, text="128 px", variable=self.width_var, value=128).grid(
            row=0, column=2, padx=2, pady=5
        )
        ttk.Radiobutton(frame, text="256 px", variable=self.width_var, value=256).grid(
            row=0, column=3, padx=2, pady=5
        )
        ttk.Button(
            frame,
            text="Set width (and update IMG_W)",
            command=self.on_set_width,
        ).grid(row=0, column=4, padx=5, pady=5, sticky="w")

        # Clear memory
        ttk.Button(
            frame,
            text="Clear memory",
            command=self.on_clear_memory,
        ).grid(row=0, column=5, padx=5, pady=5, sticky="w")

    def _build_text_frame(self):
        frame = ttk.LabelFrame(self, text="Text command (commands_set_text)")
        frame.pack(fill="both", expand=False, padx=10, pady=5)

        info = (
            "Enter text with tokens, e.g.:\n"
            "{font_sserif7}{color_rg}EASE - {color_red}Effortless "
            "{color_yellow}Algorithmic {color_rainbow1}Solution {color_rainbow2}Evolution{wait_5s}"
        )
        ttk.Label(frame, text=info, justify="left").pack(anchor="w", padx=5, pady=5)

        # --- token buttons ---
        tokens_frame = ttk.LabelFrame(frame, text="Insert tokens into text")
        tokens_frame.pack(fill="x", padx=5, pady=5)

        row = 0
        for group_name, tokens in self.token_groups.items():
            group_label = ttk.Label(tokens_frame, text=group_name + ":")
            group_label.grid(row=row, column=0, padx=5, pady=2, sticky="w")

            col = 1
            for token in tokens:
                btn = ttk.Button(
                    tokens_frame,
                    text=token,
                    command=lambda t=token: self.insert_token(t),
                    width=max(10, len(token) // 2),
                )
                btn.grid(row=row, column=col, padx=2, pady=2, sticky="w")
                col += 1

            row += 1

        # --- text editor ---
        self.text_editor = scrolledtext.ScrolledText(frame, height=5, wrap="word")
        self.text_editor.pack(fill="both", expand=True, padx=5, pady=5)
        self.text_editor.insert(
            "1.0",
            "{font_sserif7}{color_rg}EASE - {color_red}Effortless "
            "{color_yellow}Algorithmic {color_rainbow1}Solution {color_rainbow2}Evolution{wait_5s}"
        )

        ttk.Button(frame, text="Send text to panel", command=self.on_send_text).pack(
            anchor="e", padx=5, pady=5
        )

    def _build_custom_frames_frame(self):
        frame = ttk.LabelFrame(
            self, text="Custom frames (commands_show_custom_imgs + generate_led_frames)"
        )
        frame.pack(fill="x", padx=10, pady=5)

        # text for frames (allows diacritics)
        ttk.Label(frame, text="Text for custom frames (UTF-8, diacritics allowed):").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.frames_text_var = tk.StringVar(value="Příliš žluťoučký kůň úpěl ďábelské ódy.")
        ttk.Entry(frame, textvariable=self.frames_text_var, width=60).grid(
            row=0, column=1, columnspan=4, padx=5, pady=5, sticky="we"
        )

        # size
        ttk.Label(frame, text="Size:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.size_var = tk.StringVar(value="full")
        ttk.Combobox(
            frame,
            textvariable=self.size_var,
            values=["small", "medium", "full"],
            width=10,
            state="readonly",
        ).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # color
        ttk.Label(frame, text="Color:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.color_var = tk.StringVar(value="red")
        ttk.Combobox(
            frame,
            textvariable=self.color_var,
            values=["red", "green", "yellow"],
            width=10,
            state="readonly",
        ).grid(row=1, column=3, padx=5, pady=5, sticky="w")

        # font path (optional)
        ttk.Label(frame, text="Font file (optional, TTF/OTF):").grid(
            row=2, column=0, padx=5, pady=5, sticky="e"
        )
        self.font_path_var = tk.StringVar(value="")
        ttk.Entry(frame, textvariable=self.font_path_var, width=60).grid(
            row=2, column=1, columnspan=3, padx=5, pady=5, sticky="we"
        )
        ttk.Button(frame, text="Browse...", command=self.on_browse_font).grid(
            row=2, column=4, padx=5, pady=5, sticky="w"
        )

        # send button
        ttk.Button(
            frame,
            text="Generate frames and send to panel",
            command=self.on_send_custom_frames,
        ).grid(row=3, column=0, columnspan=5, padx=5, pady=10, sticky="e")

        # make columns stretch
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)
        frame.columnconfigure(3, weight=0)

    def _build_log_frame(self):
        frame = ttk.LabelFrame(self, text="Log")
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        # malý toolbar nahoře
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=(5, 0))

        # tlačítko na test logu
        ttk.Button(
            toolbar,
            text="Test log",
            command=lambda: self.log("Testovací zpráva do logu.\n"),
        ).pack(side="right", padx=5)

        # samotné textové pole logu
        self.log_widget = scrolledtext.ScrolledText(
            frame,
            height=10,
            wrap="word",
            state="disabled",
        )
        self.log_widget.pack(fill="both", expand=True, padx=5, pady=5)

    # ------------------------------------------------------------------ helpers
    def log(self, text: str):
        self.log_widget.configure(state="normal")
        self.log_widget.insert("end", text)
        self.log_widget.see("end")
        self.log_widget.configure(state="normal")

    def _open_serial(self):
        port = self.port_var.get().strip()
        if not port:
            raise RuntimeError("Serial port is empty.")
        try:
            baud = int(self.baud_var.get())
        except ValueError:
            raise RuntimeError("Baudrate must be an integer.")

        try:
            ser = serial.Serial(port=port, baudrate=baud, timeout=3)
        except Exception as e:
            raise RuntimeError(f"Cannot open port {port}: {e}")
        return ser

    def send_commands(self, commands):
        """
        Send list of bytes commands over serial and log the communication.
        """
        try:
            ser = self._open_serial()
        except RuntimeError as e:
            messagebox.showerror("Serial error", str(e))
            return

        self.log(f"\n=== Sending {len(commands)} command(s) ===\n")
        self.log(f"Port: {ser.port}, baudrate: {ser.baudrate}\n")

        for i, cmd in enumerate(commands, start=1):
            if isinstance(cmd, str):
                data = cmd.encode("ascii")
            else:
                data = cmd

            try:
                ser.write(data)
            except Exception as e:
                self.log(f"Error sending command {i}: {e}\n")
                break

            self.log(f"[{i}] Sent ({len(data)} bytes): {data.hex(' ')}\n")

            # wait briefly & try to read answer (if any)
            time.sleep(0.1)
            try:
                resp = ser.readline()
            except Exception as e:
                self.log(f"Read error: {e}\n")
                break

            if resp:
                try:
                    text = resp.decode(errors="ignore").strip()
                except Exception:
                    text = repr(resp)
                self.log(f"    Received: {text}\n")
            else:
                self.log("    No response (timeout)\n")

        ser.close()
        self.log("=== Done, port closed ===\n")

    def insert_token(self, token: str):
        """
        Insert a token into the text editor at the current cursor position.
        """
        self.text_editor.insert(tk.INSERT, token)
        self.text_editor.focus_set()

    # ------------------------------------------------------------------ callbacks
    def on_set_time_date(self):
        try:
            commands = commands_set_time_and_date()
        except Exception as e:
            messagebox.showerror("Error", f"Error building time/date command:\n{e}")
            return
        self.send_commands(commands)

    def on_set_width(self):
        width = self.width_var.get()

        if width not in (128, 256):
            messagebox.showerror("Error", "Supported widths are 128 or 256 pixels.")
            return

        # --- IMPORTANT: also update constants.IMG_W so all matrix conversions use the new width
        constants.IMG_W = width
        self.log(f"\nUpdated constants.IMG_W to {width}.\n")

        try:
            commands = commands_set_width(width)
        except Exception as e:
            messagebox.showerror("Error", f"Error building width command:\n{e}")
            return

        self.send_commands(commands)

    def on_clear_memory(self):
        try:
            commands = commands_clear_memory()
        except Exception as e:
            messagebox.showerror("Error", f"Error building clear-memory command:\n{e}")
            return
        self.send_commands(commands)

    def on_send_text(self):
        text = self.text_editor.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Empty text", "Please enter some text first.")
            return
        try:
            commands = commands_set_text(text)
        except Exception as e:
            messagebox.showerror("Error", f"Error building text command:\n{e}")
            return
        self.send_commands(commands)

    def on_browse_font(self):
        path = filedialog.askopenfilename(
            title="Select font file",
            filetypes=[
                ("Font files", "*.ttf *.otf *.ttc"),
                ("All files", "*.*"),
            ],
        )
        if path:
            self.font_path_var.set(path)

    def on_send_custom_frames(self):
        text = self.frames_text_var.get()
        if not text.strip():
            messagebox.showwarning("Empty text", "Please enter text for custom frames.")
            return

        size_label = self.size_var.get()
        color_name = self.color_var.get()
        font_path = self.font_path_var.get().strip() or None

        try:
            frames = generate_led_frames(
                text=text,
                size_label=size_label,
                color_name=color_name,
                font_path=font_path,
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error generating frames:\n{e}")
            return

        if not frames:
            messagebox.showwarning("No frames", "No frames were generated.")
            return

        self.log(f"Generated {len(frames)} frame(s) for custom text.\n")

        try:
            commands = commands_show_custom_imgs(frames)
        except Exception as e:
            messagebox.showerror("Error", f"Error building custom image commands:\n{e}")
            return

        self.send_commands(commands)


if __name__ == "__main__":
    app = SigmaPanelApp()
    app.mainloop()
