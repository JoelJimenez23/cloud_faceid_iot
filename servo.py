import serial
import time
import argparse

arduino_port = '/dev/ttyACM0'
baud_rate = 9600
arduino = serial.Serial(arduino_port,baud_rate,timeout=.1)

parser = argparse.ArgumentParser()
parser.add_argument("--degree")
args = parser.parse_args()


def write_read(x):
    arduino.write(bytes(x,  'utf-8'))
    time.sleep(0.05)
    data = arduino.readline().decode()
    return data

def func():
    while True:
        num = str(args.degree)
        value = write_read(num)
        if value != "":
            break
    return True

if __name__ == '__main__':
    print(func())



