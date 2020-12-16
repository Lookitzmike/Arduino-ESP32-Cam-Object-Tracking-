import serial
import time

# Change port to whatever arduino connected to
serialcomm = serial.Serial('COM3', 9600)

time.sleep(2)
num = 0


serialcomm.write(str(num).encode())


#     i = input("input(on/off): ").strip()
#     if i == 'q':
#         print("Program Finished")
#         break
#     serialcomm.write((i + '\n').encode())
#     time.sleep(0.5)
#     print(serialcomm.readline().decode('ascii')[:-1])
# serialcomm.close()
