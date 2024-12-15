#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

// Create an MPU6050 object
Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // Initialize the MPU6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip. Please check your connections.");
    while (1);
  }

  Serial.println("MPU6050 found!");

  // Configure the sensor
  mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  delay(100);
}

void loop() {
  // Get new sensor events with the latest data
  sensors_event_t accel, gyro, temp;
  mpu.getEvent(&accel, &gyro, &temp);

  // Map the accelerometer data to a range for Processing
  float mappedX = map(accel.acceleration.x, -10, 10, -100, 100);
  float mappedY = map(accel.acceleration.y, -10, 10, -100, 100);

  // Send data over serial as comma-separated values
  Serial.print(mappedX);
  Serial.print(",");
  Serial.println(mappedY);

  delay(50); // Slight delay for smoother output
}
