# Arduino MPU6050 Motion Tracking Project

A real-time motion tracking and visualization system using the MPU6050 IMU (Inertial Measurement Unit) sensor with Arduino and Python. This project captures accelerometer and gyroscope data to track movement and visualize motion in real-time using Pygame.

## Table of Contents
- [Overview](#overview)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Wiring Diagram](#wiring-diagram)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Scripts Description](#scripts-description)
- [Known Issues](#known-issues)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

## Overview

This project explores motion sensing and real-time visualization using the MPU6050 6-axis accelerometer and gyroscope sensor. The system:
- Captures real-time accelerometer and gyroscope data from MPU6050
- Applies noise reduction using moving average filters
- Integrates acceleration data to derive velocity and position
- Visualizes motion using Pygame graphics
- Analyzes sensor data with matplotlib plots

**Current Status:** Experimental project exploring sensor accuracy and motion integration techniques.

## Hardware Requirements

- **Arduino Board** (Uno, Nano, or compatible)
- **MPU6050 IMU Sensor** (6-axis accelerometer + gyroscope)
- **USB Cable** for Arduino connection
- **Jumper Wires** for connections

## Software Requirements

- **Arduino IDE** (1.8.x or later)
- **Python 3.7+**
- **Required Arduino Libraries:**
  - Adafruit MPU6050
  - Adafruit Unified Sensor
  - Wire (included with Arduino IDE)

- **Required Python Libraries:**
  - pyserial
  - pygame
  - numpy
  - matplotlib

See `requirements.txt` for Python dependencies.

## Installation

### 1. Install Arduino Libraries

Open Arduino IDE and install via Library Manager:
```
Tools > Manage Libraries...
```
Search and install:
- "Adafruit MPU6050"
- "Adafruit Unified Sensor"

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Upload Arduino Sketch

1. Open `arduinoCode/arduinoCode.ino` in Arduino IDE
2. Select your board: `Tools > Board`
3. Select your port: `Tools > Port`
4. Click Upload

### 4. Configure Serial Port

Update the serial port in Python scripts to match your system:
- **macOS**: `/dev/cu.usbmodem*` or `/dev/tty.usbmodem*`
- **Linux**: `/dev/ttyACM*` or `/dev/ttyUSB*`
- **Windows**: `COM3`, `COM4`, etc.

Edit `config.py` to set your serial port (see [Configuration](#configuration)).

## Wiring Diagram

Connect the MPU6050 to your Arduino:

```
MPU6050          Arduino
--------         -------
VCC      ---->   3.3V or 5V
GND      ---->   GND
SCL      ---->   A5 (or SCL)
SDA      ---->   A4 (or SDA)
```

**Note:** Some MPU6050 modules work with both 3.3V and 5V. Check your module specifications.

## Project Structure

```
arduinoProjects/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── config.py                          # Configuration settings
├── .gitignore                         # Git ignore rules
│
├── arduinoCode/                       # Arduino sketches
│   ├── arduinoCode.ino               # Main sketch (X/Y acceleration)
│   └── onlyAcceleration/
│       └── onlyAcceleration.ino      # Test sketch (X-axis only)
│
└── targetgame/                        # Python scripts
    ├── arduinoGame.py                # Real-time gyroscope visualization
    ├── test.py                       # Data analysis with plots
    ├── arduinoAcceleration.py        # Acceleration-based visualization
    ├── arduinoPassover.py            # Serial data dump utility
    └── calibration.py                # Sensor calibration utility
```

## Usage

### Quick Start

1. **Upload Arduino sketch** (one-time setup)
2. **Connect Arduino** via USB
3. **Run a Python script:**

```bash
# Real-time visualization
python targetgame/arduinoGame.py

# Data analysis with plots
python targetgame/test.py

# Sensor calibration
python targetgame/calibration.py
```

Press `Ctrl+C` to stop any script.

## Scripts Description

### Arduino Sketches

#### `arduinoCode.ino` (Main Sketch)
- Reads X and Y axis acceleration from MPU6050
- Outputs format: `x_accel,y_accel` (CSV)
- Sampling rate: 20 Hz (50ms interval)
- Baud rate: 115200
- Acceleration range: ±16G (mapped to -100 to +100)

#### `onlyAcceleration.ino` (Test Sketch)
- Simplified version for testing
- Outputs only X-axis acceleration
- Higher sampling rate: 1000 Hz (1ms interval)
- Used for sensor testing and validation

### Python Scripts

#### `arduinoGame.py` - Real-time Gyroscope Visualization
**Purpose:** Interactive dot movement based on gyroscope readings

**Features:**
- Real-time visualization using Pygame
- Integrates angular velocity to position
- 500x500 pixel window
- Red dot follows sensor motion

**Usage:**
```bash
python targetgame/arduinoGame.py
```

#### `test.py` - Data Analysis & Plotting
**Purpose:** Comprehensive data logging with visualization

**Features:**
- Applies 5-sample moving average filter
- Integrates acceleration → velocity → position
- Generates 4-subplot matplotlib graphs:
  1. X-axis: Raw vs filtered acceleration
  2. Y-axis: Raw vs filtered acceleration
  3. X-axis position over time
  4. Y-axis position over time

**Usage:**
```bash
python targetgame/test.py
# Move the sensor, then press Ctrl+C to see plots
```

#### `arduinoAcceleration.py` - Acceleration Visualization
**Purpose:** Simple horizontal dot movement based on acceleration

**Usage:**
```bash
python targetgame/arduinoAcceleration.py
```

#### `arduinoPassover.py` - Debug Utility
**Purpose:** Serial data passthrough for debugging

**Usage:**
```bash
python targetgame/arduinoPassover.py
```
Prints 1999 lines of raw serial data to console.

#### `calibration.py` - Sensor Calibration
**Purpose:** Detect and compensate for sensor drift/offset

**Usage:**
```bash
python targetgame/calibration.py
```
Place sensor on flat surface and follow prompts.

## Known Issues

### MPU6050 Sensor Accuracy
- **Double integration drift:** Integrating acceleration twice (to get position) accumulates error over time
- **Sensor noise:** Raw readings contain significant noise, requiring filtering
- **Baseline drift:** Small constant offsets cause position to drift even when stationary

**Mitigation strategies implemented:**
- 5-sample moving average filter
- Reduced sampling rate to decrease noise
- Calibration utilities

### Serial Port Configuration
- Serial port is currently hardcoded in individual scripts
- Use `config.py` to centralize configuration

## Troubleshooting

### "Serial port not found" error
1. Check Arduino is connected via USB
2. Verify port in Device Manager (Windows) or `ls /dev/tty*` (macOS/Linux)
3. Update serial port in `config.py`

### No data received
1. Ensure Arduino sketch is uploaded
2. Check baud rate matches (115200)
3. Try resetting Arduino
4. Run `arduinoPassover.py` to verify data flow

### Pygame window doesn't open
- Ensure pygame is installed: `pip install pygame`
- Check for display/graphics driver issues

### Import errors
- Install all dependencies: `pip install -r requirements.txt`
- Verify Python version: `python --version` (3.7+)

### MPU6050 not detected
1. Check wiring connections
2. Verify I2C address (usually 0x68)
3. Test with I2C scanner sketch
4. Some modules need pull-up resistors on SDA/SCL

## Future Improvements

- [ ] Implement Kalman filter for better noise reduction
- [ ] Add complementary filter for gyroscope/accelerometer fusion
- [ ] Automatic serial port detection
- [ ] GUI for configuration and real-time monitoring
- [ ] Data logging to CSV files
- [ ] 3D visualization of motion
- [ ] Gesture recognition
- [ ] Sensor fusion with magnetometer
- [ ] Better position tracking algorithms

## License

This project is open source and available for educational purposes.

## Acknowledgments

- Uses Adafruit MPU6050 library
- Motion tracking concepts from IMU sensor integration literature
- Noise reduction using moving average filters

---

**Note:** This is an experimental/learning project. Sensor accuracy limitations are documented in commit history.