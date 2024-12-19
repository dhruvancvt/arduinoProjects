import time
import serial
import numpy as np
import matplotlib.pyplot as plt
from collections import deque


arduino = serial.Serial('/dev/cu.usbmodem1423201', 115200)


accel_data_x = []
accel_data_y = []
time_data = []
moving_avg_data_x = []
moving_avg_data_y = []
posdata_x = []
posdata_y = []
time_data_pos = []  
vx = 0
vy = 0
x = 0
y = 0


WINDOW_SIZE = 5
rolling_window_x = deque(maxlen=WINDOW_SIZE)
rolling_window_y = deque(maxlen=WINDOW_SIZE)


t = time.time()

try:
    while True:
        try:

            line = arduino.readline().decode('utf-8').strip()
            ax_new, ay_new = map(float, line.split(','))  

            t_new = time.time()


            rolling_window_x.append(ax_new)
            rolling_window_y.append(ay_new)
            accel_data_x.append(ax_new)
            accel_data_y.append(ay_new)
            time_data.append(t_new - t)


            ax_avg = sum(rolling_window_x) / len(rolling_window_x)
            ay_avg = sum(rolling_window_y) / len(rolling_window_y)
            moving_avg_data_x.append(ax_avg)
            moving_avg_data_y.append(ay_avg)

            if len(time_data) >= 2:
                vx = np.trapz(accel_data_x, time_data)
                vy = np.trapz(accel_data_y, time_data)
                x = np.trapz([0, vx], time_data)
                y = np.trapz([0, vy], time_data)
                posdata_x.append(x)
                posdata_y.append(y)
                time_data_pos.append(t_new - t)  

                formattedTime = format(t_new - t, ".3f")
                formattedAX = format(ax_avg, ".2f")
                formattedAY = format(ay_avg, ".2f")
                formattedVX = format(vx, ".2f")
                formattedVY = format(vy, ".2f")
                formattedX = format(x, ".2f")
                formattedY = format(y, ".2f")

                print(f"Δt: {formattedTime} s | ax: {formattedAX} m/s² | ay: {formattedAY} m/s² | vx: {formattedVX} m/s | vy: {formattedVY} m/s | x: {formattedX} m | y: {formattedY} m")

        except KeyboardInterrupt:
            print("Program stopped by the user.")
            break

finally:

    arduino.close()

    plt.figure(figsize=(12, 14))


    plt.subplot(4, 1, 1)
    plt.plot(time_data, accel_data_x, label='Original Acceleration Data (X)', alpha=0.5)
    plt.plot(time_data, moving_avg_data_x, label=f'{WINDOW_SIZE}-Sample Moving Average (X)', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.title('X-Axis: Original vs Moving Average Acceleration Data')
    plt.legend()
    plt.grid(True)


    plt.subplot(4, 1, 2)
    plt.plot(time_data, accel_data_y, label='Original Acceleration Data (Y)', alpha=0.5)
    plt.plot(time_data, moving_avg_data_y, label=f'{WINDOW_SIZE}-Sample Moving Average (Y)', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.title('Y-Axis: Original vs Moving Average Acceleration Data')
    plt.legend()
    plt.grid(True)


    plt.subplot(4, 1, 3)
    plt.plot(time_data_pos, posdata_x, label='X Position', color='tab:blue')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.title('X-Axis: Position Over Time')
    plt.legend()
    plt.grid(True)

    plt.subplot(4, 1, 4)
    plt.plot(time_data_pos, posdata_y, label='Y Position', color='tab:orange')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.title('Y-Axis: Position Over Time')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
