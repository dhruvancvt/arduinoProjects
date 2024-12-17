#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;


sensors_event_t accelEvent, gyroEvent, tempEvent;


unsigned long previousMillis = 0;

void setup() {
  Serial.begin(115200);  // Set baud rate to match the Python script
  Wire.begin();
  
  if (!mpu.begin()) {
    while (1);  // Halt if MPU6050 is not detected
  }

  delay(100);  // Allow some time for initialization
}

void loop() {
  // Get the current time to calculate deltaTime
  unsigned long currentMillis = millis();
  float deltaTime = (currentMillis - previousMillis) / 1000.0;
  previousMillis = currentMillis;

  // Read the sensor events (accelerometer, gyroscope, and temperature)
  mpu.getEvent(&accelEvent, &gyroEvent, &tempEvent);
  
  // Print the x-axis acceleration value
  Serial.println(accelEvent.acceleration.z);

  delay(50);  // Delay between readings (adjust as needed)
}
