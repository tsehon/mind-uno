import serial
import paho.mqtt.client as mqtt
import time

uno = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
uno.reset_input_buffer()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Broker connection successful")
    else:
        print("Connection failed with result code: " +str(rc))
    
if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(host="68.181.32.115", port=11000, keepalive=60)
    client.loop_start()

    while True:
        if uno.in_waiting > 0:
            data = uno.readline().decode('utf-8').rstrip()
            client.publish("pi/brainwaves", data)
            print(data)
        time.sleep(1)
