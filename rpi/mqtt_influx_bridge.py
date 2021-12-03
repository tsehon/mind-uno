#import libraries
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import datetime
import time

#defining global variables for influxdb and mqtt
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
    
    #creates the database if it does not exist
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influx_client.create_database(INFLUXDB_DATABASE)
    
    influx_client.switch_database(INFLUXDB_DATABASE)

#Callback code that checks if client receives a CONNACK response from the server and subscribes to a topic
def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code " + str(rc))

    #subscribes to brainwave topic
    client.subscribe("pi/brainwaves")
    client.message_callback_add("pi/brainwaves", brainwaves_callback)

#creates a custom callback for brainwaves topic
def brainwaves_callback(client, userdata, message):

    data = str(message.payload, "utf-8") #gets payload data from the topic
    
    #creates a json structure to fit into Grafana
    json_body = [
            {
                'measurement': 'brainwave',
                'tags': {
                    },
                'time': datetime.datetime.now().isoformat(),
                'fields': {
                    "error": data.split(',')[0],        #first column of data gives the percent error of the data collected
                    "attention": data.split(',')[1],    #second column of data gives attention measurements from brainwaves
                    "meditation": data.split(',')[2]    #third column of data gives meditation measurements from brainwaves
                    }
                }
            ]

    #prints out the json body structure
    print(json_body)
    #writes the json structure to the influxdb database
    influx_client.write_points(json_body)

#default message callback
def on_message(client, userdata, msg):
    print(str(msg.payload, "utf-8"))

if __name__ == '__main__':
    influx_database_init() #initializes influxdb database

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

    #one second delay in between
    while True:
        time.sleep(1)

