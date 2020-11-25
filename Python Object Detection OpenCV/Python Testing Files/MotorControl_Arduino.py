import serial
import time

serialcomm = serial.Serial('COM3', 9600)    # Change port to whatever arduino connected to
serialcomm.timeout = 1

while True:
    i = input("input(on/off): ").strip()
    if i == 'q':
        print("Program Finished")
        break
    serialcomm.write((i + '\n').encode()) 
    time.sleep(0.5)
    print(serialcomm.readline().decode('ascii')[:-1])
serialcomm.close()