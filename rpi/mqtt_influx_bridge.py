import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import datetime
import time

INFLUXDB_ADDRESS = 'localhost'
INFLUXDB_USER = 'admin'
INFLUXDB_PASSWORD = 'password'
INFLUXDB_DATABASE = 'eeg'

MQTT_ADDRESS = '68.181.32.115'
MQTT_PORT = 11000
MQTT_TOPIC = 'pi/brainwaves'
    
influx_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)


def influx_database_init():
    
    databases = influx_client.get_list_database()
    
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influx_client.create_database(INFLUXDB_DATABASE)
    
    influx_client.switch_database(INFLUXDB_DATABASE)


def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code " + str(rc))
    client.subscribe("pi/brainwaves")
    client.message_callback_add("pi/brainwaves", brainwaves_callback)


def brainwaves_callback(client, userdata, message):

    data = str(message.payload, "utf-8")
    
    json_body = [
            {
                'measurement': 'brainwave',
                'tags': {
                    },
                'time': datetime.datetime.now().isoformat(),
                'fields': {
                    "error": data.split(',')[0],
                    "attention": data.split(',')[1],
                    "meditation": data.split(',')[2]
                    }
                }
            ]

    print(json_body)
    influx_client.write_points(json_body)

def on_message(client, userdata, msg):
    print(str(msg.payload, "utf-8"))

if __name__ == '__main__':
    influx_database_init()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_messsage = on_message
    client.connect(MQTT_ADDRESS, MQTT_PORT, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)

