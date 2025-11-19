#!/usr/bin/env python3

import serial
import serial.tools.list_ports


def list_ports():
    print("Available serial ports:")
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("  (no serial ports found)")
    for p in ports:
        print(f"  {p.device} - {p.description}")


def test_port(port_name, baudrate=9600):
    print(f"\nTesting port {port_name} at {baudrate} bps...")
    try:
        with serial.Serial(
            port=port_name,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
        ) as ser:

            print(f"  Opened:     {ser.port}")
            print(f"  is_open:    {ser.is_open}")
            print(f"  baudrate:   {ser.baudrate}")

            # Try to read status lines (not all adapters support this)
            try:
                print(f"  CTS: {ser.cts}, DSR: {ser.dsr}, RI: {ser.ri}, CD: {ser.cd}")
            except OSError:
                print("  (line status not supported by this driver)")

            # Optional: send 1 test byte, just to see if TX works
            test_bytes = b"\x00"
            sent = ser.write(test_bytes)
            ser.flush()
            print(f"  Sent {sent} byte(s) of test data.")

            print("  Port test finished OK.")
    except serial.SerialException as e:
        print(f"ERROR: Could not open {port_name}: {e}")


if __name__ == "__main__":
    list_ports()
    port_name = input("\nEnter port to test (e.g. COM3 or /dev/ttyUSB0): ").strip()
    if port_name:
        test_port(port_name)
    else:
        print("No port specified, exiting.")
