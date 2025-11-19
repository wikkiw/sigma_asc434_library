import serial
import time

import constants
from comm_library import commands_show_custom_imgs, commands_set_time_and_date, commands_set_width, \
    commands_clear_memory, commands_set_text
from text_to_frames import generate_led_frames, save_red_channel_bitmaps

def send_commands(commands: list[str] = []):
    # Configure serial port
    ser = serial.Serial(
        port="COM4",  # Change to your port, e.g. "/dev/ttyUSB0"
        baudrate=9600,
        timeout=3  # seconds to wait for response
    )

    print("Starting communication...\n")

    for cmd in commands:
        ser.write(cmd)

        print(f"Sent: {cmd}")

        # wait for device to respond
        time.sleep(0.1)  # small delay if needed
        response = ser.readline().decode(errors="ignore").strip()

        if response:
            print(f"Received: {response}\n")
        else:
            print("No response (timeout)\n")

    ser.close()
    print("Communication finished.")

def main():


    # Send current date & time
    # commands = commands_set_time_and_date()
    # send_commands(commands)

    # Set europe characters
    # commands = commands_set_europe_chars()

    # Set brightness
    # commands = commands_set_brightness(50)

    # Send custom img
    # img = [[0]*128 for _ in range(16)]
    #
    # for i in range(0,1):
    #     img[i][i] = 1
    #     img[i][i+1] = 1
    #
    # commands = commands_show_custom_imgs([(img, img)])

    # commands = commands_clear_memory()
    # send_commands(commands)
    #
    # commands = commands_set_width(constants.IMG_W)
    # send_commands(commands)
    #
    #commands = commands_set_text("{action_none}{font_serif12}{color_red}E{color_green}A{color_yellow}S{color_rainbow1}E-{font_serif7}{color_red}Effortless {color_green}Algorithmic {color_yellow}Solution {color_rainbow1}Evolution")
    commands = commands_set_text("{action_holdt}{font_sserif7}{color_green}What: {color_gr}frontEASE{wait_0s}{next_frame}{action_holdb}{font_sserif7}{color_red}By: {color_rg}Jozef Kovac{wait_5s}{next_frame}{action_holdt}{font_sserif7}{color_green}What: {color_gr}EASE{wait_0s}{next_frame}{action_holdb}{font_sserif7}{color_red}By: {color_rg}Tomas Kadavy & Adam Viktorin{wait_5s}")
    send_commands(commands)

    # # Send text
    # frames = generate_led_frames(
    #     text="EASE - Effortless Algorithmic Solution Evolution",
    #     size_label="full",
    #     color_name="green"
    # )
    #
    # print("Number of frames:", len(frames))
    # save_red_channel_bitmaps(frames, output_dir="test_bitmaps")
    #
    # commands = commands_show_custom_imgs(frames)
    # send_commands(commands)

if __name__ == "__main__":
    main()