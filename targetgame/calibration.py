"""
MPU6050 Sensor Calibration Utility

This script helps calibrate the MPU6050 sensor by detecting the baseline offset
values when the sensor is at rest. These offsets can then be subtracted from
future readings to improve accuracy.

The calibration process:
1. Place sensor on a flat, stable surface
2. Keep sensor completely still during calibration
3. Script collects samples and calculates average offset
4. Offsets are saved to a JSON file for use in other scripts

Usage:
    python calibration.py
"""

import serial
import time
import json
import sys
import os
import numpy as np

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import config
except ImportError:
    print("Warning: config.py not found. Using default values.")
    class config:
        SERIAL_PORT = '/dev/cu.usbmodem1423201'
        BAUD_RATE = 115200
        CALIBRATION_SAMPLES = 100
        CALIBRATION_FILE = 'sensor_calibration.json'


def collect_calibration_data(ser, num_samples):
    """
    Collect calibration data from the sensor.

    Args:
        ser: Serial connection object
        num_samples: Number of samples to collect

    Returns:
        tuple: (x_values, y_values) lists of collected data
    """
    x_values = []
    y_values = []

    print(f"\nCollecting {num_samples} samples...")
    print("Keep sensor COMPLETELY STILL on a flat surface!")
    print("\nProgress: ", end='', flush=True)

    samples_collected = 0
    while samples_collected < num_samples:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line and ',' in line:
                # Parse X,Y values
                x_str, y_str = line.split(',')
                x_val = float(x_str)
                y_val = float(y_str)

                x_values.append(x_val)
                y_values.append(y_val)
                samples_collected += 1

                # Progress indicator
                if samples_collected % 10 == 0:
                    print(f"{samples_collected}", end=' ', flush=True)

            elif line:
                # Single value (X-axis only)
                x_val = float(line)
                x_values.append(x_val)
                y_values.append(0.0)  # No Y data
                samples_collected += 1

                if samples_collected % 10 == 0:
                    print(f"{samples_collected}", end=' ', flush=True)

        except (ValueError, UnicodeDecodeError) as e:
            # Skip invalid data
            continue

    print("\n\nData collection complete!")
    return x_values, y_values


def calculate_statistics(values, axis_name):
    """
    Calculate statistics for calibration values.

    Args:
        values: List of sensor readings
        axis_name: Name of the axis (for display)

    Returns:
        dict: Statistics including mean, std, min, max
    """
    mean = np.mean(values)
    std = np.std(values)
    min_val = np.min(values)
    max_val = np.max(values)

    print(f"\n{axis_name}-Axis Statistics:")
    print(f"  Mean (Offset):     {mean:8.4f}")
    print(f"  Std Deviation:     {std:8.4f}")
    print(f"  Min Value:         {min_val:8.4f}")
    print(f"  Max Value:         {max_val:8.4f}")
    print(f"  Range:             {max_val - min_val:8.4f}")

    return {
        'mean': mean,
        'std': std,
        'min': min_val,
        'max': max_val,
        'range': max_val - min_val
    }


def save_calibration(x_offset, y_offset, x_stats, y_stats, filename):
    """
    Save calibration data to JSON file.

    Args:
        x_offset: X-axis offset value
        y_offset: Y-axis offset value
        x_stats: X-axis statistics dictionary
        y_stats: Y-axis statistics dictionary
        filename: Output filename
    """
    calibration_data = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'offsets': {
            'x': float(x_offset),
            'y': float(y_offset)
        },
        'statistics': {
            'x_axis': {k: float(v) for k, v in x_stats.items()},
            'y_axis': {k: float(v) for k, v in y_stats.items()}
        },
        'samples_collected': config.CALIBRATION_SAMPLES
    }

    with open(filename, 'w') as f:
        json.dump(calibration_data, f, indent=4)

    print(f"\nCalibration data saved to: {filename}")


def load_calibration(filename):
    """
    Load calibration data from JSON file.

    Args:
        filename: Calibration file path

    Returns:
        dict: Calibration data or None if file doesn't exist
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def display_calibration_info(cal_data):
    """
    Display existing calibration information.

    Args:
        cal_data: Calibration data dictionary
    """
    print("\nExisting Calibration Data:")
    print(f"  Created: {cal_data['timestamp']}")
    print(f"  X Offset: {cal_data['offsets']['x']:.4f}")
    print(f"  Y Offset: {cal_data['offsets']['y']:.4f}")
    print(f"  Samples: {cal_data['samples_collected']}")


def main():
    """Main calibration routine."""

    print("=" * 70)
    print("MPU6050 Sensor Calibration Utility")
    print("=" * 70)
    print(f"\nSerial Port: {config.SERIAL_PORT}")
    print(f"Baud Rate: {config.BAUD_RATE}")
    print(f"Samples to collect: {config.CALIBRATION_SAMPLES}")

    # Check for existing calibration
    existing_cal = load_calibration(config.CALIBRATION_FILE)
    if existing_cal:
        display_calibration_info(existing_cal)
        print("\nWarning: Existing calibration will be overwritten!")

    print("\n" + "=" * 70)
    print("IMPORTANT CALIBRATION INSTRUCTIONS:")
    print("=" * 70)
    print("1. Place the MPU6050 sensor on a FLAT, STABLE surface")
    print("2. Ensure the sensor is LEVEL (use a spirit level if available)")
    print("3. Keep the sensor COMPLETELY STILL during calibration")
    print("4. Avoid vibrations, bumps, or movement near the sensor")
    print("5. This will take approximately", config.CALIBRATION_SAMPLES // 20, "seconds")
    print("=" * 70)

    input("\nPress Enter when sensor is ready and stable...")

    # Connect to Arduino
    try:
        ser = serial.Serial(config.SERIAL_PORT, config.BAUD_RATE)
        print(f"\nConnected to Arduino on {config.SERIAL_PORT}")

        # Wait for Arduino to stabilize
        print("Waiting 2 seconds for sensor to stabilize...")
        time.sleep(2)

        # Clear any buffered data
        ser.reset_input_buffer()

        # Collect calibration data
        x_values, y_values = collect_calibration_data(ser, config.CALIBRATION_SAMPLES)

        # Calculate offsets and statistics
        print("\n" + "=" * 70)
        print("Calibration Results")
        print("=" * 70)

        x_stats = calculate_statistics(x_values, "X")
        y_stats = calculate_statistics(y_values, "Y")

        x_offset = x_stats['mean']
        y_offset = y_stats['mean']

        # Quality assessment
        print("\n" + "=" * 70)
        print("Calibration Quality Assessment")
        print("=" * 70)

        x_quality = "Good" if x_stats['std'] < 2.0 else "Poor - sensor was not stable"
        y_quality = "Good" if y_stats['std'] < 2.0 else "Poor - sensor was not stable"

        print(f"X-Axis Quality: {x_quality}")
        print(f"Y-Axis Quality: {y_quality}")

        if x_stats['std'] >= 2.0 or y_stats['std'] >= 2.0:
            print("\nWarning: High standard deviation detected!")
            print("This indicates the sensor was not completely still.")
            print("Consider re-running calibration for better results.")
            retry = input("\nRetry calibration? (y/n): ")
            if retry.lower() == 'y':
                ser.close()
                main()
                return

        # Save calibration
        print("\n" + "=" * 70)
        save_calibration(x_offset, y_offset, x_stats, y_stats, config.CALIBRATION_FILE)

        print("\n" + "=" * 70)
        print("Calibration Complete!")
        print("=" * 70)
        print("\nTo use these offsets in your scripts:")
        print("  1. Load the calibration file")
        print("  2. Subtract offsets from sensor readings:")
        print(f"     corrected_x = raw_x - {x_offset:.4f}")
        print(f"     corrected_y = raw_y - {y_offset:.4f}")
        print("\nExample Python code:")
        print("  import json")
        print(f"  with open('{config.CALIBRATION_FILE}', 'r') as f:")
        print("      cal = json.load(f)")
        print("  x_corrected = raw_x - cal['offsets']['x']")
        print("  y_corrected = raw_y - cal['offsets']['y']")
        print("=" * 70)

        ser.close()

    except serial.SerialException as e:
        print(f"\nError: Could not open serial port {config.SERIAL_PORT}")
        print(f"Details: {e}")
        print("\nTroubleshooting:")
        print("1. Check that Arduino is connected via USB")
        print("2. Verify the correct port in config.py")
        print("3. Ensure Arduino sketch is uploaded")
        print("4. Try running: python config.py (to diagnose issues)")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nCalibration interrupted by user.")
        ser.close()
        sys.exit(0)


if __name__ == '__main__':
    main()
