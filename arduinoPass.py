import serial
import time
import threading
import pygame
import sys

# Global variables
running = True
dot_position = [250, 250]  # Initial position of the dot

def readserial(comport, baudrate, timestamp=False):
    global running, dot_position
    ser = serial.Serial(comport, baudrate, timeout=0.1)

    while running:
        data = ser.readline().decode().strip()
        if data:
            if timestamp:
                current_time = time.strftime('%H:%M:%S')
                print(f'{current_time} > {data}')
            else:
                print(data)

            # Update dot position if data is in 'x,y' format
            try:
                x, y = map(int, data.split(","))
                dot_position[0] = x
                dot_position[1] = y
            except ValueError:
                pass  # Ignore invalid data

    ser.close()
    print("Serial connection closed.")

def stop_reading():
    global running
    input("Press Enter to stop the serial reading...")
    running = False

def draw_moving_dot():
    global running, dot_position

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Serial Dot Movement")

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the dot
        pygame.draw.circle(screen, (255, 0, 0), dot_position, 10)

        # Refresh the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    # Start the serial reading thread
    threading.Thread(target=stop_reading).start()
    threading.Thread(target=readserial, args=('/dev/cu.usbmodem1423201', 115200, True)).start()
    draw_moving_dot()
