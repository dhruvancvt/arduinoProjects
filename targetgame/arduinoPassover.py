"""
Arduino Serial Passthrough Utility

A simple debugging utility that reads raw serial data from the Arduino
and prints it to the console. Useful for verifying serial communication
and checking data format.

Usage:
    python arduinoPassover.py

This script will print 1999 lines of serial data from the Arduino.
"""

import serial
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import config
except ImportError:
    print("Warning: config.py not found. Using default values.")
    class config:
        SERIAL_PORT = '/dev/cu.usbmodem1423201'
        BAUD_RATE = 115200


def main():
    """Main function to read and display serial data."""

    print("=" * 60)
    print("Arduino Serial Passthrough")
    print("=" * 60)
    print(f"Port: {config.SERIAL_PORT}")
    print(f"Baud Rate: {config.BAUD_RATE}")
    print("Reading 1999 lines of data...")
    print("Press Ctrl+C to stop early")
    print("=" * 60 + "\n")

    try:
        # Connect to Arduino
        arduino = serial.Serial(config.SERIAL_PORT, config.BAUD_RATE)
        print(f"Connected to Arduino on {config.SERIAL_PORT}\n")

        # Read 1999 lines
        lines_to_read = 1999
        lines_read = 0

        try:
            while lines_read < lines_to_read:
                # Read data from Arduino and decode to string
                data = arduino.readline().decode('utf-8').strip()
                if data:  # Only print non-empty lines
                    print(f"[{lines_read + 1:4d}] {data}")
                    lines_read += 1

        except KeyboardInterrupt:
            print(f"\n\nInterrupted by user after {lines_read} lines.")

        finally:
            arduino.close()
            print(f"\n{'=' * 60}")
            print(f"Total lines read: {lines_read}")
            print("Serial connection closed.")
            print("=" * 60)

    except serial.SerialException as e:
        print(f"\nError: Could not open serial port {config.SERIAL_PORT}")
        print(f"Details: {e}")
        print("\nTroubleshooting:")
        print("1. Check that Arduino is connected via USB")
        print("2. Verify the correct port in config.py")
        print("3. Ensure Arduino sketch is uploaded")
        print("4. Try running: python config.py (to diagnose issues)")
        sys.exit(1)


if __name__ == '__main__':
    main()
