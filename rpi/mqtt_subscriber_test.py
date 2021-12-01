import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code " + str(rc))
    client.subscribe("pi/brainwaves")
    client.message_callback_add("pi/brainwaves", brainwaves_callback)

def brainwaves_callback(client, userdata, message):
    print("VM: " + str(message.payload, "utf-8"))

def on_message(client, userdata, msg):
    print(str(msg.payload, "utf-8"))

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_messsage = on_message
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_forever()

    while True:
        time.sleep(1)

