"""Receive MAX30102 Red/IR raw ADC samples over ESP32 serial and save as CSV."""

import argparse
import csv
import sys
import time
from datetime import datetime
from pathlib import Path

import serial
from serial.tools import list_ports


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Record ESP32 + MAX30102 PPG raw data (Red/IR) as CSV."
    )
    parser.add_argument("--list-ports", action="store_true", help="List serial ports")
    parser.add_argument("--port", help="Windows: COM5; macOS: /dev/cu.usbserial-...")
    parser.add_argument("--seconds", type=float, help="Recording duration; omit for Ctrl+C")
    parser.add_argument("--output", help="CSV path; default is a timestamped filename")
    args = parser.parse_args()

    if args.list_ports:
        ports = sorted(list_ports.comports(), key=lambda item: item.device)
        if not ports:
            print("No serial ports found. Check your USB data cable and driver.")
        for port in ports:
            print(f"{port.device}  {port.description}")
        return 0

    if not args.port:
        parser.error("--port is required (or use --list-ports)")
    if args.seconds is not None and args.seconds <= 0:
        parser.error("--seconds must be greater than zero")

    output = Path(
        args.output or f"ppg_raw_{datetime.now():%Y%m%d_%H%M%S}.csv"
    ).expanduser()

    count = 0
    try:
        with serial.Serial(args.port, 115200, timeout=0.25) as stream:
            # Some ESP32 boards reset automatically when the serial port opens.
            print(f"Connected to {args.port}; waiting for ESP32 to start...")
            time.sleep(2)

            # Exclusive creation prevents accidental loss of previous data.
            with output.open("x", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["sample", "red", "ir"])

                print(f"Recording to {output}. Press Ctrl+C to stop.")
                start = time.monotonic()
                try:
                    while args.seconds is None or time.monotonic() - start < args.seconds:
                        line = stream.readline().decode("ascii", errors="ignore").strip()
                        fields = line.split(",")
                        if len(fields) != 3 or not all(value.isdecimal() for value in fields):
                            if line.startswith("# ERROR"):
                                print(line, file=sys.stderr)
                            continue

                        writer.writerow([int(value) for value in fields])
                        count += 1
                        if count % 100 == 0:
                            file.flush()
                            print(f"{count} samples saved; latest: {line}")
                except KeyboardInterrupt:
                    print("\nRecording stopped by user.")

        print(f"Done: {count} samples -> {output}")
        if not count:
            print("No sample received. Check sensor wiring and firmware.", file=sys.stderr)
            return 1
        return 0
    except FileExistsError:
        print(f"File already exists: {output}. Choose a new --output name.", file=sys.stderr)
        return 1
    except serial.SerialException as exc:
        print(f"Serial port error: {exc}", file=sys.stderr)
        print("Close the PlatformIO Serial Monitor before recording.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
