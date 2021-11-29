import serial

uno = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
uno.reset_input_buffer()

while True:
    if uno.in_waiting > 0:
        data = uno.readline().decode('utf-8').rstrip()
        print(data)
