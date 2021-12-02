import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code " + str(rc))
    client.subscribe("pi/brainwaves")
    client.message_callback_add("pi/brainwaves", brainwaves_callback)

def brainwaves_callback(client, userdata, message):
    print("Data: " + str(message.payload, "utf-8"))
#    json_body = [
#            {
#                'measurement': brainwave,
#                'tags': {
#                    },
#                'time': datetime.datetime.now().isoformat(),
#                'fields': {
#                    "error": _error,
#                    "attention": _attention,
#                    "meditation": _meditation
#                    }
#                }
#            ]
#    client.write_points(json_body)

def on_message(client, userdata, msg):
    print(str(msg.payload, "utf-8"))

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_messsage = on_message
    client.connect(host="68.181.32.115", port=11000, keepalive=60)
    client.loop_forever()

    while True:
        time.sleep(1)

