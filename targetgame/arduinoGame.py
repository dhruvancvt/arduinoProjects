import serial
import time
import threading
import pygame
import sys

# Global variables
running = True
dot_position = [250, 250]  # Initial position of the dot
invalid_data = None  # To store the most recent invalid data

def readserial(comport, baudrate, timestamp=False):
    global running, dot_position, invalid_data
    ser = serial.Serial(comport, baudrate, timeout=0.1)

    while running:
        data = ser.readline().decode().strip()
        if data:
            if timestamp:
                current_time = time.strftime('%H:%M:%S')
                print(f'{current_time} > {data}')
            else:
                print(data)

            # Try updating dot position with valid data
            try:
                x, y = map(int, data.split(","))
                dot_position[0] = x
                dot_position[1] = y
                invalid_data = None  # Reset invalid data on success
            except ValueError:
                invalid_data = data  # Store the invalid data
                print(f"Invalid Data, using fallback: {invalid_data}")
                use_invalid_data_to_move(invalid_data)

    ser.close()
    print("Serial connection closed.")

def use_invalid_data_to_move(data):
    """Fallback function to move the dot using invalid data."""
    global dot_position
    try:
        # If the data is a single integer, use it to move along the x-axis
        value = int(data)
        dot_position[0] = max(0, min(500, dot_position[0] + value))
    except ValueError:
        # If data is non-numeric, use the ASCII sum of the characters
        ascii_sum = sum(ord(char) for char in data)
        dot_position[0] = max(0, min(500, dot_position[0] + ascii_sum % 20))
        dot_position[1] = max(0, min(500, dot_position[1] + ascii_sum % 20))

def stop_reading():
    global running
    input("Press Enter to stop the serial reading...")
    running = False

def draw_moving_dot():
    global running, dot_position, invalid_data

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Serial Dot Movement")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the dot
        pygame.draw.circle(screen, (255, 0, 0), dot_position, 10)

        # Display invalid data if it exists
        if invalid_data:
            text_surface = font.render(f"Invalid Data: {invalid_data}", True, (255, 255, 255))
            screen.blit(text_surface, (10, 10))

        # Refresh the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    # Start the serial reading thread
    threading.Thread(target=stop_reading).start()
    threading.Thread(target=readserial, args=('/dev/cu.usbmodem1443201', 115200, True)).start()
    draw_moving_dot()
