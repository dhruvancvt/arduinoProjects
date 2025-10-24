"""
MPU6050 Data Analysis and Plotting

This script collects acceleration data from the MPU6050 sensor, applies
a moving average filter, and generates comprehensive plots showing:
- Raw vs filtered acceleration (X and Y axes)
- Position over time (derived from double integration)

Usage:
    python test.py
    (Move the sensor around, then press Ctrl+C to display plots)
"""

import time
import serial
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import config
except ImportError:
    print("Warning: config.py not found. Using default values.")
    class config:
        SERIAL_PORT = '/dev/cu.usbmodem1423201'
        BAUD_RATE = 115200
        WINDOW_SIZE = 5
        PLOT_FIGURE_WIDTH = 12
        PLOT_FIGURE_HEIGHT = 14

# Initialize serial connection with error handling
try:
    arduino = serial.Serial(config.SERIAL_PORT, config.BAUD_RATE)
    print(f"Connected to Arduino on {config.SERIAL_PORT}")
    print(f"Collecting data with {config.WINDOW_SIZE}-sample moving average...")
    print("Move the sensor around. Press Ctrl+C when done to see plots.\n")
except serial.SerialException as e:
    print(f"Error: Could not open serial port {config.SERIAL_PORT}")
    print(f"Details: {e}")
    print("\nTroubleshooting:")
    print("1. Check that Arduino is connected via USB")
    print("2. Verify the correct port in config.py")
    print("3. Ensure Arduino sketch is uploaded")
    print(f"4. Try running: python config.py (to diagnose issues)")
    sys.exit(1)


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


# Use window size from config
rolling_window_x = deque(maxlen=config.WINDOW_SIZE)
rolling_window_y = deque(maxlen=config.WINDOW_SIZE)


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
    # Close serial connection
    arduino.close()
    print("\n\nSerial connection closed.")
    print(f"Collected {len(time_data)} data points.")
    print("Generating plots...\n")

    # Create plots with configured figure size
    plt.figure(figsize=(config.PLOT_FIGURE_WIDTH, config.PLOT_FIGURE_HEIGHT))


    plt.subplot(4, 1, 1)
    plt.plot(time_data, accel_data_x, label='Original Acceleration Data (X)', alpha=0.5)
    plt.plot(time_data, moving_avg_data_x, label=f'{config.WINDOW_SIZE}-Sample Moving Average (X)', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.title('X-Axis: Original vs Moving Average Acceleration Data')
    plt.legend()
    plt.grid(True)


    plt.subplot(4, 1, 2)
    plt.plot(time_data, accel_data_y, label='Original Acceleration Data (Y)', alpha=0.5)
    plt.plot(time_data, moving_avg_data_y, label=f'{config.WINDOW_SIZE}-Sample Moving Average (Y)', linewidth=2)
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
