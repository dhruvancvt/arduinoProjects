#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// Create MPU6050 object
Adafruit_MPU6050 mpu;

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);
  
  // Initialize I2C communication with MPU6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  // Set accelerometer range
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);

  // Set sample rate
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  delay(100);
}

void loop() {
  // Get new sensor event
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Extract X and Y acceleration values and send over serial
  Serial.print(a.acceleration.x);
  Serial.print(",");
  Serial.println(a.acceleration.y);

  delay(100);  // Adjust the delay as needed
}
