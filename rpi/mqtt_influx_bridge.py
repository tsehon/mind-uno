import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import datetime
import time

# global variables for influxdb and mqtt
INFLUXDB_ADDRESS = 'localhost'
INFLUXDB_USER = 'admin'
INFLUXDB_PASSWORD = 'password'
INFLUXDB_DATABASE = 'eeg'

MQTT_ADDRESS = '68.181.32.115'
MQTT_PORT = 11000
MQTT_TOPIC = 'pi/brainwaves'

#initializes influxdb client server    
influx_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

#initializes the influxdb database from the influxdb client server
def influx_database_init():
    
    databases = influx_client.get_list_database()
    
    #creates a new influxdb database if it does not exist already
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influx_client.create_database(INFLUXDB_DATABASE)
    
    influx_client.switch_database(INFLUXDB_DATABASE)

#Callback code that checks if client receives a CONNACK response from the server and subscribes to a topic
def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code " + str(rc))

    #subscribes to brainwaves topic
    client.subscribe("pi/brainwaves")
    client.message_callback_add("pi/brainwaves", brainwaves_callback)

# custom callback for incoming eeg (brainwave) data 
def brainwaves_callback(client, userdata, message):

    data = str(message.payload, "utf-8")
    
    json_body = [
            {
                'measurement': 'brainwave',
                'tags': {

                    },
                'time': datetime.datetime.now().isoformat(),
                'fields': {
                    "signal strength": data.split(',')[0],        #first column of data gives fidelity of the data 
                    "attention": data.split(',')[1],    #second column of data gives attention measurements from brainwaves
                    "meditation": data.split(',')[2]    #third column of data gives meditation measurements from brainwaves
                    }
                }
            ]
    
    print(json_body)

    #writes the json to the influxdb database
    influx_client.write_points(json_body)

#default message callback
def on_message(client, userdata, msg):
    print(str(msg.payload, "utf-8"))

if __name__ == '__main__':

    #initialize influxdb database
    influx_database_init() 

    #creates a client object
    client = mqtt.Client()

    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect

    #attach the on_message() callback function defined above to the mqtt client
    client.on_messsage = on_message

    #connect to mqtt server and port, which is same as eclipse.usc.edu host and port 
    client.connect(MQTT_ADDRESS, MQTT_PORT, keepalive=60)
    
    #starts loop to have paho-mqtt create a separate thread to handle incoming and outgoing mqtt messages
    client.loop_start()

    while True:
        time.sleep(1)

