import serial
import subprocess

arduino_port = '/dev/ttyUSB0'
baud_rate = 9600
ser = serial.Serial(arduino_port,baud_rate)

def testing():
    contador0 = 0
    contador1 = 0
    while True:
        message = ser.readline().decode('utf-8').strip()
        print(" message: ",message," contador: ",contador0);
        if message == "0" and contador0 == 0:
            contador1 = 0
            hola = subprocess.run(['python3','camera_recognition.py'])
            contador0+=1
            print("RESULTADO DE HOLA",hola)
            subprocess.run(['python3','servo_manipulation.py'])
        elif message == "1" and contador1 == 0:
            contador0 = 0
            ord('q')
            contador1+=1

testing()

