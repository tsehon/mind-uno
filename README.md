# MindUno: An IoT System to Collect and Visualize Brianwave Data
### Contributors: 
Tyler Sehon, Victor Muljo
### **Demo Link:** https://drive.google.com/file/d/1gvVWAInyaOYTnaAPWKdwba9XMVyLUbCn/view?usp=sharing

## **Brief Description and Motivation:**

The purpose of our IoT system, “MindUno”, is to collect raw brainwave data by means of electroencephalography and communicate that data to a node (our laptop) in order to visualize the data in a meaningful, human-understandable way.


## **Components, Protocols, and Processing:**
The “MindUno” is composed of an ArduinoUno electrical-taped to a Mindflex headband with a soldered Rx and GND connection.
The Arduino sets up a Serial object for the Mindflex device to read in its raw EEG data, and enters a loop where it then polls the Mindflex data, processes it using the Arduino Brain library, and sends that data over serial to a RaspberryPi. The Arduino Brain library parses the raw brainwave data from the Mindflex into comma-separated values (signal strength, attention, meditation, etc.) to send over serial to the RaspberryPi.
From our virtual machine, we SSH into the RaspberryPi, where we run rpi_publish.py. This python program retrieves and decodes the incoming data from the ArduinoUno, then publishes it using the MQTT protocol, ready to be fetched on our virtual machine. The MQTT broker used is eclipse.usc.edu:11000, and we set up our client using the paho-mqtt-client library.

On our virtual machine, we run mqtt_influx_bridge.py. This program initializes an InfluxDB client and database (using the InfluxDB-Python library), as well as an MQTT client to interact with our broker (eclipse.usc.edu:11000). The program connects to the server and subscribes to the appropriate topic (“pi/brainwaves”), for which a custom callback is defined. This custom callback is triggered each time the RaspberryPi publishes brainwave data to the topic, where it decodes the payload and parses the data into a json body, and then writes that json body to the InfluxDB database.
A grafana server, hosted on our virtual machine at localhost:3000, is then used to visualize the data in our InfluxDB database. For this, we have a simple dashboard that displays the meditation and attention values.

Throughout the process of completing this project, our most consistent limitation stemmed from the outdated hardware of the Mindflex headset, which resulted in inconsistent signal strength and thereby improper/inaccurate brainwave data measured by the headset. Oftentimes, we would have a high-fidelity signal (0 on a 0-200 scale, where 200 means signal failure and 0 a successful connection). Other times, the Mindflex consistently read a poor EEG signal (the NeuroSky chipset inside the Mindflex, which we solder our connection to, tells us how strong the signal is). When this happened, the data was unreliable and would have to be treated as garbage values.

## Libraries used:
- [Paho MQTT Client](https://github.com/eclipse/paho.mqtt.python)
- [Serial](https://pythonhosted.org/pyserial/index.html)
- [time](https://docs.python.org/3/library/time.html)
- [datetime](https://docs.python.org/3/library/datetime.html#module-datetime)
- [InfluxDB Client](https://github.com/influxdata/influxdb-python)
- [Arduino Brain Library](https://github.com/kitschpatrol/Brain.git)
