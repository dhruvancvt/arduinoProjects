import time
import serial
import numpy as np
from collections import deque


arduino = serial.Serial('/dev/cu.usbmodem1423201', 115200)


acceleration_data = []
time_data = []
vx = 0
x = 0

WINDOW_SIZE = 50  
rolling_window = deque(maxlen=WINDOW_SIZE)

# Start time
t = time.time()

while True:
    try:

        ax_new = float(arduino.readline().decode('utf-8').strip())
        t_new = time.time()


        rolling_window.append(ax_new)


        ax_avg = sum(rolling_window) / len(rolling_window)


        acceleration_data.append(ax_avg)
        time_data.append(t_new)

        if len(time_data) >= 2:

            vx = np.trapz(acceleration_data, time_data)


            x = np.trapz([0, vx], time_data)


            formattedTime = format(t_new - t, ".3f")
            formattedAX = format(ax_avg, ".2f")
            formattedVX = format(vx, ".2f")
            formattedX = format(x, ".2f")

            print(f"Δt: {formattedTime} s | ax: {formattedAX} m/s² | vx: {formattedVX} m/s | x: {formattedX} m")

        t = t_new

    except KeyboardInterrupt:
        print("Program stopped by the user.")
        break
