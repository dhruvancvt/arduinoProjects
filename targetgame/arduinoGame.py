"""
Arduino MPU6050 Real-Time Gyroscope Visualization

This script provides real-time visualization of gyroscope data from the MPU6050
sensor. A red dot moves on screen based on angular velocity readings, demonstrating
the integration of gyroscope data to determine position changes.

Usage:
    python arduinoGame.py

Controls:
    - Close window or press Enter in terminal to exit
"""

import serial
import threading
import pygame
import sys
import time
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
        SERIAL_TIMEOUT = 0.1
        WINDOW_WIDTH = 500
        WINDOW_HEIGHT = 500
        DOT_RADIUS = 10
        DOT_COLOR = (255, 0, 0)
        BACKGROUND_COLOR = (0, 0, 0)
        PYGAME_FPS = 30
        GYRO_SCALING_FACTOR = 10

# Global variables
running = True
dot_position = [config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2]  # Initial position (center)

# Variables to hold previous time for delta time calculation
previous_time = time.time()
x_velocity = 0  # Initialize x velocity (angular velocity to position conversion)
y_velocity = 0  # Initialize y velocity (angular velocity to position conversion)

def readserial(comport, baudrate):
    """
    Read serial data from Arduino in a separate thread.

    Args:
        comport: Serial port path
        baudrate: Communication baud rate
    """
    global running, dot_position, previous_time, x_velocity, y_velocity

    try:
        ser = serial.Serial(comport, baudrate, timeout=config.SERIAL_TIMEOUT)
        print(f"Connected to Arduino on {comport}")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        print("\nTroubleshooting:")
        print("1. Check that Arduino is connected via USB")
        print("2. Verify the correct port in config.py")
        print("3. Ensure Arduino sketch is uploaded")
        running = False
        return

    while running:
        try:
            data = ser.readline().decode().strip()
            if data:
                print(f"Received Data: {data}")  # Debug: print the received data
                try:
                    # Parse the received data (assuming format: 'x,y')
                    x, y = map(float, data.split(","))
                    
                    # Calculate delta time (time between updates)
                    current_time = time.time()
                    delta_time = current_time - previous_time
                    previous_time = current_time
                    
                    # Debug: print the delta_time and x, y values
                    print(f"Delta Time: {delta_time}, x: {x}, y: {y}")

                    # Integrate gyroscope data (angular velocity to change in position)
                    x_velocity += x * delta_time * config.GYRO_SCALING_FACTOR  # Apply scaling factor
                    y_velocity += y * delta_time * config.GYRO_SCALING_FACTOR  # Apply scaling factor

                    # Debug: print the updated velocities
                    print(f"Updated Velocities -> x_velocity: {x_velocity}, y_velocity: {y_velocity}")

                    # Update the dot position, apply bounds to keep the dot within screen limits
                    dot_position[0] = max(0, min(config.WINDOW_WIDTH, dot_position[0] + int(y_velocity)))
                    dot_position[1] = max(0, min(config.WINDOW_HEIGHT, dot_position[1] + int(x_velocity)))

                    # Debug: print the updated dot position
                    print(f"Updated Dot Position -> x: {dot_position[0]}, y: {dot_position[1]}")
                    
                except ValueError:
                    print(f"Invalid data received: {data}")

        except serial.SerialException as e:
            print(f"Serial error: {e}")
            running = False

    ser.close()
    print("Serial connection closed.")


def stop_reading():
    global running
    input("Press Enter to stop the program...\n")
    running = False


def draw_moving_dot():
    """
    Draw the moving dot visualization using Pygame.
    Runs in the main thread.
    """
    global running, dot_position

    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption("MPU6050 Gyroscope - Real-Time Motion")

    clock = pygame.time.Clock()

    print("Pygame window opened. Move your sensor!")
    print("Close window or press Enter in terminal to exit.\n")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(config.BACKGROUND_COLOR)  # Clear the screen
        pygame.draw.circle(screen, config.DOT_COLOR, dot_position, config.DOT_RADIUS)  # Draw the dot

        pygame.display.flip()
        clock.tick(config.PYGAME_FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    """Main entry point for the gyroscope visualization."""

    print("=" * 60)
    print("MPU6050 Gyroscope Real-Time Visualization")
    print("=" * 60)
    print(f"Serial Port: {config.SERIAL_PORT}")
    print(f"Baud Rate: {config.BAUD_RATE}")
    print("=" * 60 + "\n")

    try:
        # Start serial reading thread
        serial_thread = threading.Thread(target=readserial, args=(config.SERIAL_PORT, config.BAUD_RATE))
        serial_thread.daemon = True  # Make thread daemon so it exits when main exits
        serial_thread.start()

        # Start stop reading thread
        stop_thread = threading.Thread(target=stop_reading)
        stop_thread.daemon = True
        stop_thread.start()

        # Run pygame visualization in main thread
        draw_moving_dot()

        # Wait for threads to complete
        serial_thread.join()
        stop_thread.join()

    except KeyboardInterrupt:
        running = False
        print("\nProgram interrupted by user.")
    finally:
        print("\nClosing application. Goodbye!")
