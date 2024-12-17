#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

// Variables to store gyroscope data
sensors_event_t accelEvent, gyroEvent, tempEvent;

// Previous time for calculating delta time
unsigned long previousMillis = 0;

void setup() {
  Serial.begin(115200);  // Set baud rate to match the Python script
  Wire.begin();
  
  if (!mpu.begin()) {
    Serial.println("Failed to detect and initialize MPU6050 sensor!");
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
  
  // Scale down the gyro values (depending on the default range, which is likely ±250 degrees per second)
  int deltaX = gyroEvent.gyro.x / 10;  // Adjust divisor for appropriate sensitivity
  int deltaY = gyroEvent.gyro.y / 10;
  
  // Send the data to the serial port in comma-separated format
  Serial.print(deltaX);
  Serial.print(",");
  Serial.println(deltaY);
  
  delay(50);  // Delay between readings (adjust as needed)
}

