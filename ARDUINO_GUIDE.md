# Arduino MPU6050 Sketches Guide

This document provides detailed information about the Arduino sketches used in this project. The actual `.ino` files are excluded from git (see `.gitignore`) but are documented here for reference.

## Table of Contents
- [Hardware Setup](#hardware-setup)
- [Library Dependencies](#library-dependencies)
- [Main Sketch: arduinoCode.ino](#main-sketch-arduinocodeino)
- [Test Sketch: onlyAcceleration.ino](#test-sketch-onlyaccelerationino)
- [Configuration Options](#configuration-options)
- [Troubleshooting](#troubleshooting)
- [Data Format](#data-format)

---

## Hardware Setup

### Components Required
- Arduino board (Uno, Nano, Mega, or compatible)
- MPU6050 IMU sensor module
- USB cable for programming and communication
- Jumper wires

### Wiring Connections

```
MPU6050 Pin    →    Arduino Pin
-----------         -----------
VCC            →    3.3V or 5V (check your module)
GND            →    GND
SCL            →    A5 (or dedicated SCL pin)
SDA            →    A4 (or dedicated SDA pin)
```

**Important Notes:**
- Some MPU6050 modules have onboard voltage regulators and work with both 3.3V and 5V
- Other modules require exactly 3.3V - **check your module datasheet**
- The I2C pins on different Arduino boards:
  - **Uno/Nano**: A4 (SDA), A5 (SCL)
  - **Mega**: Pin 20 (SDA), Pin 21 (SCL)
  - **Leonardo**: Pin 2 (SDA), Pin 3 (SCL)

### I2C Address
- Default MPU6050 I2C address: **0x68**
- Alternative address (if AD0 pin is HIGH): **0x69**

---

## Library Dependencies

The Arduino sketches require the following libraries. Install them via the Arduino IDE Library Manager:

### 1. Adafruit MPU6050
```
Library Manager → Search: "Adafruit MPU6050"
Version: 2.0.0 or later
```

### 2. Adafruit Unified Sensor
```
Library Manager → Search: "Adafruit Unified Sensor"
Version: 1.1.0 or later
```

### 3. Wire (Built-in)
The Wire library for I2C communication is included with Arduino IDE.

### Installation Steps
1. Open Arduino IDE
2. Go to `Tools` → `Manage Libraries...`
3. Search for "Adafruit MPU6050"
4. Click "Install"
5. When prompted, click "Install All" to also install dependencies

---

## Main Sketch: arduinoCode.ino

### Location
```
arduinoCode/arduinoCode.ino
```

### Purpose
The main sketch that reads **both X and Y axis** acceleration data from the MPU6050 and transmits it via serial in CSV format.

### Code Overview

```cpp
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);

  // Initialize MPU6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }

  // Configure sensor ranges
  mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  Serial.println("MPU6050 Ready");
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Map acceleration values from range [-16, 16] to [-100, 100]
  float mappedX = map(a.acceleration.x * 100, -1600, 1600, -100, 100);
  float mappedY = map(a.acceleration.y * 100, -1600, 1600, -100, 100);

  // Output format: "x,y"
  Serial.print(mappedX);
  Serial.print(",");
  Serial.println(mappedY);

  delay(50);  // 20 Hz sampling rate
}
```

### Configuration Settings

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Baud Rate** | 115200 | Serial communication speed |
| **Accelerometer Range** | ±16G | Maximum acceleration measurable |
| **Gyroscope Range** | ±500°/s | Maximum angular velocity |
| **Filter Bandwidth** | 21 Hz | Low-pass filter cutoff frequency |
| **Sampling Rate** | 20 Hz | Data output frequency (50ms delay) |
| **Output Range** | -100 to +100 | Mapped acceleration values |

### Output Format
```
<x_acceleration>,<y_acceleration>\n
```

**Example output:**
```
-5.23,12.45
-4.87,11.98
-5.01,12.15
```

### Key Features
- ✓ Dual-axis (X and Y) acceleration measurement
- ✓ Value mapping for easier processing
- ✓ 20 Hz output rate (good balance between speed and accuracy)
- ✓ CSV format for easy parsing

---

## Test Sketch: onlyAcceleration.ino

### Location
```
arduinoCode/onlyAcceleration/onlyAcceleration.ino
```

### Purpose
A simplified testing sketch that outputs **only X-axis** acceleration data at a higher sampling rate. Useful for debugging and validating sensor operation.

### Code Overview

```cpp
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;
unsigned long previousTime = 0;

void setup() {
  Serial.begin(115200);

  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  Serial.println("MPU6050 Ready - X-axis only");
}

void loop() {
  unsigned long currentTime = millis();
  unsigned long deltaTime = currentTime - previousTime;

  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Output only X-axis
  Serial.println(a.acceleration.x);

  previousTime = currentTime;
  delay(1);  // 1000 Hz sampling rate
}
```

### Configuration Settings

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Baud Rate** | 115200 | Serial communication speed |
| **Accelerometer Range** | ±16G | Maximum acceleration measurable |
| **Gyroscope Range** | ±500°/s | Maximum angular velocity |
| **Filter Bandwidth** | 21 Hz | Low-pass filter cutoff frequency |
| **Sampling Rate** | ~1000 Hz | High-speed data output (1ms delay) |
| **Output** | Raw acceleration | X-axis only, no mapping |

### Output Format
```
<x_acceleration>\n
```

**Example output:**
```
-0.52
-0.48
-0.51
```

### Key Features
- ✓ Single-axis (X) acceleration measurement
- ✓ Raw acceleration values (in m/s²)
- ✓ High-speed sampling (1000 Hz)
- ✓ Includes delta time calculation for testing
- ✓ Simpler output format

### Use Cases
- Testing sensor connectivity
- Validating I2C communication
- High-frequency data collection
- Single-axis motion analysis

---

## Configuration Options

### Accelerometer Ranges

The MPU6050 supports four accelerometer sensitivity ranges:

| Range | Constant | Use Case |
|-------|----------|----------|
| ±2G | `MPU6050_RANGE_2_G` | Subtle movements, high precision |
| ±4G | `MPU6050_RANGE_4_G` | General motion tracking |
| ±8G | `MPU6050_RANGE_8_G` | Moderate impacts, sports |
| ±16G | `MPU6050_RANGE_16_G` | High impacts, vibrations **(default)** |

**To change:**
```cpp
mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
```

### Gyroscope Ranges

The MPU6050 supports four gyroscope sensitivity ranges:

| Range | Constant | Use Case |
|-------|----------|----------|
| ±250°/s | `MPU6050_RANGE_250_DEG` | Slow rotations, precision |
| ±500°/s | `MPU6050_RANGE_500_DEG` | General motion **(default)** |
| ±1000°/s | `MPU6050_RANGE_1000_DEG` | Fast rotations |
| ±2000°/s | `MPU6050_RANGE_2000_DEG` | Very fast rotations |

**To change:**
```cpp
mpu.setGyroRange(MPU6050_RANGE_1000_DEG);
```

### Filter Bandwidth

The MPU6050 has a built-in low-pass filter to reduce noise:

| Bandwidth | Constant | Noise Reduction | Response Time |
|-----------|----------|----------------|---------------|
| 260 Hz | `MPU6050_BAND_260_HZ` | Low | Fast |
| 184 Hz | `MPU6050_BAND_184_HZ` | Low | Fast |
| 94 Hz | `MPU6050_BAND_94_HZ` | Medium | Medium |
| 44 Hz | `MPU6050_BAND_44_HZ` | Medium | Medium |
| 21 Hz | `MPU6050_BAND_21_HZ` | High | Slow **(default)** |
| 10 Hz | `MPU6050_BAND_10_HZ` | Very High | Very Slow |
| 5 Hz | `MPU6050_BAND_5_HZ` | Maximum | Very Slow |

**To change:**
```cpp
mpu.setFilterBandwidth(MPU6050_BAND_44_HZ);
```

### Baud Rate

Common baud rates for serial communication:

- **9600**: Standard, slow but reliable
- **57600**: Moderate speed
- **115200**: Fast, recommended for this project **(default)**
- **230400**: Very fast, may have issues on some systems

**To change (in both Arduino and Python):**

Arduino:
```cpp
Serial.begin(230400);
```

Python (in `config.py`):
```python
BAUD_RATE = 230400
```

---

## Troubleshooting

### Sensor Not Detected

**Symptom:** Serial monitor shows "Failed to find MPU6050 chip"

**Solutions:**
1. Check wiring connections
2. Verify power (VCC) is connected to correct voltage (3.3V or 5V)
3. Ensure SDA and SCL are not swapped
4. Try I2C scanner sketch to detect address
5. Check for loose connections or damaged wires
6. Some MPU6050 modules need pull-up resistors (4.7kΩ) on SDA and SCL

### No Serial Output

**Symptom:** No data appears in serial monitor or Python script

**Solutions:**
1. Verify correct baud rate (115200)
2. Check USB cable is data-capable (not power-only)
3. Select correct COM port in Arduino IDE
4. Ensure sketch is uploaded successfully
5. Press reset button on Arduino
6. Check `Serial.begin()` is called in `setup()`

### Erratic or Noisy Data

**Symptom:** Readings jump around wildly, even when sensor is stationary

**Solutions:**
1. Add decoupling capacitor (0.1µF) near MPU6050 VCC and GND
2. Use shielded wires for I2C connections if long (>10cm)
3. Reduce filter bandwidth (use 10 Hz or 5 Hz)
4. Increase moving average window size in Python scripts
5. Run calibration utility to compensate for offset
6. Keep sensor away from electromagnetic interference sources
7. Use shorter USB cable

### Incorrect Values

**Symptom:** Values are shifted or don't match expected range

**Solutions:**
1. Run calibration utility (`python calibration.py`)
2. Verify accelerometer range setting matches your application
3. Check value mapping calculations in code
4. Ensure sensor is properly mounted (flat and level)
5. Account for gravity (9.8 m/s² on Z-axis when flat)

### Communication Errors

**Symptom:** UnicodeDecodeError or serial timeout in Python

**Solutions:**
1. Add delay after `serial.Serial()` before reading
2. Use `ser.reset_input_buffer()` to clear stale data
3. Implement try-except blocks for decode errors
4. Verify matching baud rates
5. Check for electromagnetic interference

---

## Data Format

### Main Sketch Output (arduinoCode.ino)

**Format:** CSV (Comma-Separated Values)

```
<x_value>,<y_value>\n
```

**Parsing in Python:**
```python
line = ser.readline().decode('utf-8').strip()
x, y = map(float, line.split(','))
```

**Value Range:** -100 to +100 (mapped from raw ±16G range)

**Units:** Arbitrary (mapped for convenience, not physical units)

**Conversion to m/s²:**
```python
# Reverse mapping to get m/s²
x_ms2 = (x / 100.0) * 16.0 * 9.81  # ±16G range
y_ms2 = (y / 100.0) * 16.0 * 9.81
```

### Test Sketch Output (onlyAcceleration.ino)

**Format:** Single value per line

```
<x_value>\n
```

**Parsing in Python:**
```python
line = ser.readline().decode('utf-8').strip()
x = float(line)
```

**Value Range:** -16.0 to +16.0 (raw values)

**Units:** m/s² (meters per second squared)

---

## Best Practices

### For Accurate Measurements
1. **Calibrate regularly** - Run calibration utility before each session
2. **Stable mounting** - Secure sensor to prevent vibrations
3. **Warm-up period** - Let sensor stabilize for 10-15 seconds after power-on
4. **Appropriate range** - Use smallest range that covers your motion
5. **Filter properly** - Balance between responsiveness and noise

### For Development
1. **Start with test sketch** - Verify hardware before complex code
2. **Monitor serial output** - Use Arduino Serial Monitor for debugging
3. **Check current draw** - Some USB ports can't power Arduino + sensor
4. **Version control** - Although .ino files are gitignored, keep backups
5. **Document changes** - Comment your modifications

### For Production Use
1. **Error handling** - Check `mpu.begin()` return value
2. **Watchdog timer** - Reset if sensor becomes unresponsive
3. **Data validation** - Sanity-check values before sending
4. **Overflow protection** - Ensure buffers don't overflow
5. **Power management** - Consider sleep modes for battery operation

---

## Additional Resources

### Official Documentation
- [MPU6050 Datasheet](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf)
- [Adafruit MPU6050 Library](https://github.com/adafruit/Adafruit_MPU6050)
- [Arduino Wire Library](https://www.arduino.cc/en/Reference/Wire)

### Useful Tools
- **I2C Scanner**: Detect MPU6050 address ([example sketch](https://playground.arduino.cc/Main/I2cScanner/))
- **Serial Plotter**: Built into Arduino IDE (`Tools` → `Serial Plotter`)
- **Processing**: For advanced visualization

### Common Modifications

#### Add Z-Axis
```cpp
// In loop()
float mappedZ = map(a.acceleration.z * 100, -1600, 1600, -100, 100);
Serial.print(",");
Serial.println(mappedZ);
```

#### Add Gyroscope Data
```cpp
// In loop()
Serial.print(g.gyro.x);
Serial.print(",");
Serial.print(g.gyro.y);
Serial.print(",");
Serial.println(g.gyro.z);
```

#### Add Temperature
```cpp
// In loop()
Serial.print("Temp: ");
Serial.print(temp.temperature);
Serial.println(" °C");
```

---

## Summary

Both Arduino sketches provide reliable interfaces to the MPU6050 sensor:

- **arduinoCode.ino**: Production sketch for dual-axis motion tracking at 20 Hz
- **onlyAcceleration.ino**: Debug/test sketch for high-speed single-axis data

Choose the appropriate sketch based on your needs, configure the sensor parameters, and ensure proper hardware connections for best results.

For questions or issues, refer to the main [README.md](README.md) troubleshooting section.
