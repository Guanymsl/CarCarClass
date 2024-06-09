import serial
import time

arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to be established

def send_data(data):
    arduino.write((data + '\n').encode())

def receive_data():
    return arduino.readline().decode().strip()

send_data("LED")
print(receive_data())

arduino.close()

