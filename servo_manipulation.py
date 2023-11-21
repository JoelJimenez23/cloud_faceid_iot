import serial
import subprocess
import time

def testing():
    contador0 = 0
    contador1 = 0
    while True:
        message = ser.readline().decode('utf-8').strip()
        print(" message: ",message," contador: ",contador0)
        if message == "0" and contador0 == 0:
            contador1 = 0
            subprocess.run(['python3','servo.py','--degree','100'])
            contador0+=1
            print("SERVO ABIERTOOOOOO")
        elif message == "1" and contador1 == 0:
            contador0 = 0
            time.sleep(5)
            subprocess.run(['python3','servo.py','--degree','0'])
            print("SERVO CERRADOOOOOOOO")
            contador1+=1
            break

testing()
