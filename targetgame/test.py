import time
import serial

arduino = serial.Serial('/dev/cu.usbmodem1423201', 115200)
ax = 0
vx = 0
x = 0
ax_new = 0
vx_new = 0
x_new = 0
t = time.time()

while True:
    ax_new = float(arduino.readline().decode('utf-8').strip()) 
    t_new = time.time()
    deltaTime = t_new - t
    vx_new = vx + ((ax_new + ax)/2) * deltaTime
    x_new = x + ((vx_new + vx)/2) * deltaTime
    formattedDelta = format(deltaTime, ".3f")
    formattedX = format(x_new, ".2f")
    formattedax = format(ax_new, ".2f")
    print(formattedDelta, formattedax, formattedX)
    t = t_new
    ax = ax_new
    vx = vx_new
    x = x_new

    


