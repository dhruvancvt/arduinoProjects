import time
import serial
import numpy as np
import matplotlib.pyplot as plt
from collections import deque


arduino = serial.Serial('/dev/cu.usbmodem1423201', 115200)


acceleration_data = []
time_data = []
moving_avg_data = []
vx = 0
x = 0


WINDOW_SIZE = 50  
rolling_window = deque(maxlen=WINDOW_SIZE)


t = time.time()

try:
    while True:
        try:
            
            ax_new = float(arduino.readline().decode('utf-8').strip())
            t_new = time.time()

            rolling_window.append(ax_new)
            acceleration_data.append(ax_new)
            time_data.append(t_new - t)

            ax_avg = sum(rolling_window) / len(rolling_window)
            moving_avg_data.append(ax_avg)

            if len(time_data) >= 2:
                vx = np.trapz(acceleration_data, time_data)
                x = np.trapz([0, vx], time_data)
                formattedTime = format(t_new - t, ".3f")
                formattedAX = format(ax_avg, ".2f")
                formattedVX = format(vx, ".2f")
                formattedX = format(x, ".2f")

                print(f"Δt: {formattedTime} s | ax: {formattedAX} m/s² | vx: {formattedVX} m/s | x: {formattedX} m")

        except KeyboardInterrupt:
            print("Program stopped by the user.")
            break

finally:
    arduino.close()
    plt.figure(figsize=12)
    plt.plot(time_data, acceleration_data, label='Original Acceleration Data', alpha=0.5)
    plt.plot(time_data, moving_avg_data, label='Sample Moving Average', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.legend()
    plt.show()
