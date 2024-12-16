import serial

arduino = serial.Serial('/dev/cu.usbmodem1423201', 115200)
x = 20
while x < 20 and x > 0:
    try:
        data = arduino.readline().decode('utf-8').strip()
        x, y = map(float, data.split(","))
        print(f"X: {x}, Y: {y}")
        x-=1

    except ValueError:
        print(f"Invalid data received: {data}")
