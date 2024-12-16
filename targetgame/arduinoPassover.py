import serial

arduino = serial.Serial('/dev/cu.usbmodem1423201', 115200)

while True:
    try:
        data = arduino.readline().decode('utf-8').strip() #reads data from arduino and strips it to readable formal
        x, y = map(float, data.split(",")) #formats data for printing
        print(f"X: {x}, Y: {y}")
    except ValueError:
        print(f"Invalid data received: {data}")
