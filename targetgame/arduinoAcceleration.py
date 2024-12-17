import pygame
import serial
import time

delay = 50

# Initialize the serial port (adjust the port to match your system)
ser = serial.Serial('/dev/cu.usbmodem1423201', 115200, timeout=1)

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Red Dot Moving Along X-axis")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)


position = WIDTH // 2  
velocity = 0.0
previous_time = time.time()

# Pygame clock for controlling frame rate
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read acceleration data from serial
    try:
        line = ser.readline().decode('utf-8').strip()
        if line:
            acceleration = float(line)
        else:
            acceleration = 0.0
    except (ValueError, serial.SerialException):
        acceleration = 0.0

    
    velocity += acceleration * delta_time
    position += velocity * delta_time * 100 

    # Keep the position within screen bounds
    if position < 0:
        position = 0
        velocity = 0
    elif position > WIDTH:
        position = WIDTH
        velocity = 0

    # Clear the screen
    screen.fill(BLACK)

    # Draw the red dot
    pygame.draw.circle(screen, RED, (int(position), HEIGHT // 2), 10)

    # Update the display
    pygame.display.flip()

    # Control the frame rate (20 frames per second)
    clock.tick(20)

# Close the serial connection and quit Pygame
ser.close()
pygame.quit()
