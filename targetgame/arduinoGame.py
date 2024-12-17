import serial
import threading
import pygame
import sys
import time

# Global variables
running = True
dot_position = [250, 250]  # Initial position of the dot

# Variables to hold previous time for delta time calculation
previous_time = time.time()
x_velocity = 0  # Initialize x velocity (angular velocity to position conversion)
y_velocity = 0  # Initialize y velocity (angular velocity to position conversion)

# Scaling factor to amplify the small gyroscope readings
scaling_factor = 10  # Adjust this factor to make the movement more noticeable

def readserial(comport, baudrate):
    global running, dot_position, previous_time, x_velocity, y_velocity

    try:
        ser = serial.Serial(comport, baudrate, timeout=0.1)
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
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
                    x_velocity += x * delta_time * scaling_factor  # Apply scaling factor
                    y_velocity += y * delta_time * scaling_factor  # Apply scaling factor
                    
                    # Debug: print the updated velocities
                    print(f"Updated Velocities -> x_velocity: {x_velocity}, y_velocity: {y_velocity}")

                    # Update the dot position, apply bounds to keep the dot within screen limits
                    dot_position[0] = max(0, min(500, dot_position[0] + int(y_velocity)))
                    dot_position[1] = max(0, min(500, dot_position[1] + int(x_velocity)))

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
    global running, dot_position

    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Serial Dot Movement")

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Clear the screen
        pygame.draw.circle(screen, (255, 0, 0), dot_position, 10)  # Draw the dot

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    try:
        serial_thread = threading.Thread(target=readserial, args=('/dev/cu.usbmodem1443201', 115200))  # Update with your serial port
        serial_thread.start()

        stop_thread = threading.Thread(target=stop_reading)
        stop_thread.start()

        draw_moving_dot()

        serial_thread.join()
        stop_thread.join()

    except KeyboardInterrupt:
        running = False
        print("\nProgram interrupted by user.")
