#import modules
import serial
import paho.mqtt.client as mqtt
import time

uno = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
uno.reset_input_buffer()

def on_connect(client, userdata, flags, rc):
    #Checks if client receives a CONNACK response from the server, otherwise print out a failure message with result code
    if rc == 0:
        print("Broker connection successful")
    else:
        print("Connection failed with result code: " +str(rc))
    
if __name__ == '__main__':
    #creates a client object
    client = mqtt.Client() 

    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect

    #connect to eclipse.usc.edu host and port 
    client.connect(host="68.181.32.115", port=11000, keepalive=60)

    #starts loop to have paho-mqtt create a separate thread to handle incoming and outgoing mqtt messages
    client.loop_start()

    #publishes and prints messages of data retrieved
    while True:
        if uno.in_waiting > 0:
            data = uno.readline().decode('utf-8').rstrip()
            client.publish("pi/brainwaves", data)
            print(data)
        time.sleep(1)
