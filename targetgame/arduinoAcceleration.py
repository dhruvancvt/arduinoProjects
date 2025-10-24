"""
Arduino Acceleration Visualization

This script visualizes horizontal (X-axis) movement based on acceleration data
from the Arduino MPU6050 sensor. The red dot moves along a horizontal line,
with its velocity determined by integrating the acceleration values.

Usage:
    python arduinoAcceleration.py

Controls:
    - Close window or Ctrl+C to exit
"""

import pygame
import serial
import time
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import config
except ImportError:
    print("Warning: config.py not found. Using default values.")
    # Fallback configuration
    class config:
        SERIAL_PORT = '/dev/cu.usbmodem1423201'
        BAUD_RATE = 115200
        SERIAL_TIMEOUT = 1


def main():
    """Main function to run the acceleration visualization."""

    # Initialize the serial port
    try:
        ser = serial.Serial(config.SERIAL_PORT, config.BAUD_RATE, timeout=config.SERIAL_TIMEOUT)
        print(f"Connected to Arduino on {config.SERIAL_PORT}")
        print("Reading acceleration data...")
        print("Close window to exit.\n")
    except serial.SerialException as e:
        print(f"Error: Could not open serial port {config.SERIAL_PORT}")
        print(f"Details: {e}")
        print("\nTroubleshooting:")
        print("1. Check that Arduino is connected via USB")
        print("2. Verify the correct port in config.py")
        print("3. Ensure Arduino sketch is uploaded")
        sys.exit(1)

    # Initialize Pygame
    pygame.init()

    # Screen dimensions (wider horizontal view)
    WIDTH, HEIGHT = 800, 200
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MPU6050 Acceleration - Horizontal Movement")

    # Colors
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GRAY = (100, 100, 100)

    # Physics variables
    position = WIDTH // 2  # Start in center
    velocity = 0.0
    previous_time = time.time()

    # Pygame clock for controlling frame rate
    clock = pygame.time.Clock()
    FPS = 30

    # Main loop
    running = True
    try:
        while running:
            # Calculate delta time (time since last frame)
            current_time = time.time()
            delta_time = current_time - previous_time
            previous_time = current_time

            # Handle Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Read acceleration data from serial
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    # Parse acceleration value
                    # If data format is "x,y", take only first value
                    if ',' in line:
                        acceleration = float(line.split(',')[0])
                    else:
                        acceleration = float(line)
                else:
                    acceleration = 0.0
            except (ValueError, serial.SerialException) as e:
                acceleration = 0.0
                # Uncomment for debugging:
                # print(f"Serial read error: {e}")

            # Integrate acceleration to get velocity (v = v + a*dt)
            velocity += acceleration * delta_time

            # Integrate velocity to get position (x = x + v*dt)
            # Multiply by 100 to amplify movement (adjust as needed)
            position += velocity * delta_time * 100

            # Keep the position within screen bounds with damping
            if position < 0:
                position = 0
                velocity = 0  # Stop at boundary
            elif position > WIDTH:
                position = WIDTH
                velocity = 0  # Stop at boundary

            # Clear the screen
            screen.fill(BLACK)

            # Draw center reference line
            pygame.draw.line(screen, GRAY, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)

            # Draw the red dot
            pygame.draw.circle(screen, RED, (int(position), HEIGHT // 2), 10)

            # Display current values
            font = pygame.font.Font(None, 24)
            accel_text = font.render(f"Accel: {acceleration:6.2f}", True, (255, 255, 255))
            vel_text = font.render(f"Vel: {velocity:6.2f}", True, (255, 255, 255))
            pos_text = font.render(f"Pos: {int(position)}", True, (255, 255, 255))

            screen.blit(accel_text, (10, 10))
            screen.blit(vel_text, (10, 35))
            screen.blit(pos_text, (10, 60))

            # Update the display
            pygame.display.flip()

            # Control the frame rate
            clock.tick(FPS)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

    finally:
        # Cleanup
        ser.close()
        pygame.quit()
        print("Serial connection closed. Goodbye!")


if __name__ == '__main__':
    main()
