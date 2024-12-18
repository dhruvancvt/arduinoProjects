import time
import serial
import numpy as np


arduino = serial.Serial('/dev/cu.usbmodem1423201', 115200)


acceleration_data = []
time_data = []
vx = 0
x = 0

# Start time
t = time.time()

while True:
    try:
        ax_new = float(arduino.readline().decode('utf-8').strip())
        t_new = time.time()
        acceleration_data.append(ax_new)
        time_data.append(t_new)
        if len(time_data) >= 2:
            vx = np.trapz(acceleration_data, time_data)
            
            x = np.trapz([0, vx], time_data)
            
            formattedTime = format(t_new - t, ".3f")
            formattedAX = format(ax_new, ".2f")
            formattedVX = format(vx, ".2f")
            formattedX = format(x, ".2f")
            
            print(f"Δt: {formattedTime} s | ax: {formattedAX} m/s² | vx: {formattedVX} m/s | x: {formattedX} m")
        
        t = t_new

    except KeyboardInterrupt:
        print("Program stopped by the user.")
        break
