import serial
import time
import threading

running = True

def readserial(comport, baudrate, timestamp=False):
    global running
    ser = serial.Serial(comport, baudrate, timeout=0.1)

    while running:
        data = ser.readline().decode().strip()
        if data and timestamp:
            current_time = time.strftime('%H:%M:%S')
            print(f'{current_time} > {data}')
        elif data:
            print(data)

    ser.close()
    print("Serial connection closed.")

def stop_reading():
    global running
    input("Press Enter to stop the serial reading...")
    running = False

if __name__ == '__main__':
    threading.Thread(target=stop_reading).start()
    readserial('/dev/cu.usbmodem1423201', 115200, True)
