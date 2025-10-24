"""
Configuration file for Arduino MPU6050 Motion Tracking Project

This file centralizes all configurable parameters used across the Python scripts.
Modify these values to match your hardware setup and preferences.
"""

import sys
import serial.tools.list_ports


# ==============================================================================
# SERIAL PORT CONFIGURATION
# ==============================================================================

# Serial port - Update this to match your Arduino connection
# Examples:
#   macOS:   '/dev/cu.usbmodem1423201' or '/dev/tty.usbmodem*'
#   Linux:   '/dev/ttyACM0' or '/dev/ttyUSB0'
#   Windows: 'COM3' or 'COM4'
SERIAL_PORT = '/dev/cu.usbmodem1423201'

# Baud rate - Must match the Arduino sketch (default: 115200)
BAUD_RATE = 115200

# Serial timeout in seconds
SERIAL_TIMEOUT = 0.1


# ==============================================================================
# MPU6050 SENSOR CONFIGURATION
# ==============================================================================

# Accelerometer range (must match Arduino sketch settings)
# Options: 2, 4, 8, 16 (in G)
ACCEL_RANGE = 16

# Gyroscope range (must match Arduino sketch settings)
# Options: 250, 500, 1000, 2000 (in degrees/second)
GYRO_RANGE = 500

# Sensor sampling rate (Hz) - configured in Arduino sketch
SAMPLING_RATE = 20  # Hz (50ms interval in Arduino code)

# Acceleration value mapping range
# Arduino maps raw values to this range for easier processing
ACCEL_MAP_MIN = -100
ACCEL_MAP_MAX = 100


# ==============================================================================
# SIGNAL PROCESSING PARAMETERS
# ==============================================================================

# Moving average window size for noise reduction
# Larger values = smoother but more lag
WINDOW_SIZE = 5

# Scaling factor for gyroscope visualization
# Amplifies small gyroscope readings for better visibility
GYRO_SCALING_FACTOR = 10


# ==============================================================================
# VISUALIZATION SETTINGS
# ==============================================================================

# Pygame window dimensions (pixels)
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

# Dot properties for visualization
DOT_RADIUS = 10
DOT_COLOR = (255, 0, 0)  # RGB: Red

# Pygame frame rate (FPS)
PYGAME_FPS = 30

# Background color
BACKGROUND_COLOR = (0, 0, 0)  # RGB: Black


# ==============================================================================
# CALIBRATION SETTINGS
# ==============================================================================

# Number of samples to collect for calibration
CALIBRATION_SAMPLES = 100

# Calibration file path (stores offset values)
CALIBRATION_FILE = 'sensor_calibration.json'


# ==============================================================================
# PLOTTING SETTINGS (for test.py)
# ==============================================================================

# Figure size for matplotlib plots
PLOT_FIGURE_WIDTH = 12
PLOT_FIGURE_HEIGHT = 14


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def list_serial_ports():
    """
    List all available serial ports on the system.

    Returns:
        list: Available serial port names
    """
    ports = serial.tools.list_ports.comports()
    available_ports = []

    print("\nAvailable serial ports:")
    for port in ports:
        print(f"  - {port.device}: {port.description}")
        available_ports.append(port.device)

    if not available_ports:
        print("  No serial ports found!")

    return available_ports


def auto_detect_arduino_port():
    """
    Attempt to automatically detect Arduino serial port.

    Returns:
        str: Detected port name or None if not found
    """
    ports = serial.tools.list_ports.comports()

    # Common Arduino identifiers
    arduino_keywords = ['arduino', 'usbmodem', 'usbserial', 'ttyACM', 'ttyUSB', 'CH340']

    for port in ports:
        port_info = f"{port.device} {port.description}".lower()
        for keyword in arduino_keywords:
            if keyword.lower() in port_info:
                print(f"\nAuto-detected Arduino on: {port.device}")
                return port.device

    return None


def get_serial_port():
    """
    Get the serial port to use, with auto-detection fallback.

    Returns:
        str: Serial port to use
    """
    # Try configured port first
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
        ser.close()
        return SERIAL_PORT
    except serial.SerialException:
        pass

    # Try auto-detection
    detected_port = auto_detect_arduino_port()
    if detected_port:
        return detected_port

    # Fall back to listing all ports
    print(f"\nConfigured port '{SERIAL_PORT}' not available.")
    available_ports = list_serial_ports()

    if available_ports:
        print(f"\nUpdate SERIAL_PORT in config.py to one of the above ports.")

    return SERIAL_PORT  # Return configured port anyway


# ==============================================================================
# CONFIGURATION VALIDATION
# ==============================================================================

def validate_config():
    """
    Validate configuration parameters.

    Returns:
        bool: True if configuration is valid
    """
    errors = []

    # Validate accelerometer range
    if ACCEL_RANGE not in [2, 4, 8, 16]:
        errors.append(f"Invalid ACCEL_RANGE: {ACCEL_RANGE}. Must be 2, 4, 8, or 16.")

    # Validate gyroscope range
    if GYRO_RANGE not in [250, 500, 1000, 2000]:
        errors.append(f"Invalid GYRO_RANGE: {GYRO_RANGE}. Must be 250, 500, 1000, or 2000.")

    # Validate window size
    if WINDOW_SIZE < 1:
        errors.append(f"Invalid WINDOW_SIZE: {WINDOW_SIZE}. Must be at least 1.")

    # Validate baud rate
    valid_baud_rates = [9600, 19200, 38400, 57600, 115200, 230400, 250000]
    if BAUD_RATE not in valid_baud_rates:
        errors.append(f"Invalid BAUD_RATE: {BAUD_RATE}. Common values: {valid_baud_rates}")

    if errors:
        print("\nConfiguration Errors:")
        for error in errors:
            print(f"  - {error}")
        return False

    return True


# ==============================================================================
# MAIN - Run diagnostics when executed directly
# ==============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("Arduino MPU6050 Configuration Diagnostics")
    print("=" * 70)

    print("\n[1] Configuration Validation")
    if validate_config():
        print("  ✓ Configuration is valid")
    else:
        print("  ✗ Configuration has errors")
        sys.exit(1)

    print("\n[2] Serial Port Configuration")
    print(f"  Configured port: {SERIAL_PORT}")
    print(f"  Baud rate: {BAUD_RATE}")

    print("\n[3] Detecting Serial Ports")
    available_ports = list_serial_ports()

    print("\n[4] Testing Serial Connection")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=SERIAL_TIMEOUT)
        print(f"  ✓ Successfully connected to {SERIAL_PORT}")
        ser.close()
    except serial.SerialException as e:
        print(f"  ✗ Failed to connect to {SERIAL_PORT}")
        print(f"    Error: {e}")

        detected = auto_detect_arduino_port()
        if detected and detected != SERIAL_PORT:
            print(f"\n  Suggestion: Update SERIAL_PORT to '{detected}'")

    print("\n[5] Current Configuration Summary")
    print(f"  Accelerometer Range: ±{ACCEL_RANGE}G")
    print(f"  Gyroscope Range: ±{GYRO_RANGE}°/s")
    print(f"  Moving Average Window: {WINDOW_SIZE} samples")
    print(f"  Visualization Window: {WINDOW_WIDTH}x{WINDOW_HEIGHT}px")
    print(f"  Frame Rate: {PYGAME_FPS} FPS")

    print("\n" + "=" * 70)
    print("Diagnostics complete!")
    print("=" * 70)
