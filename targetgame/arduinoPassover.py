import serial

arduino = serial.Serial('/dev/cu.usbmodem1443201', 115200)
x = 20
while x < 2000 and x > 0:
    data = arduino.readline().decode('utf-8').strip() #reads data from arduino and strips it to readable formal
    print(data)
    x-=1
