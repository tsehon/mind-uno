# EE250 Final Project - Brainwave Reader
### Team Members: 
Tyler Sehon, Victor Muljo
### **Demo Link:**

## **Instructions to run code:**

1. On ArduinoUno
   _ Upload arduino_tx.ino to the ArduinoUno via the ArduinoIDE (must remove Rx for the code to allow the code to upload). 
2. On RaspberryPi, run the rpi_publish.py program:
   _ python3 rpi_publish.py
3. On virtual machine:
   _ sudo systemctl start influxdb
   _ sudo systemctl start grafana-server
   _ run mqtt_influx_bridge.py
     _ python3 mqtt_influx_bridge.py


## Libraries used:
- [Paho MQTT Client](https://github.com/eclipse/paho.mqtt.python)
- [Serial](https://pythonhosted.org/pyserial/index.html)
- [time](https://docs.python.org/3/library/time.html)
- [datetime](https://docs.python.org/3/library/datetime.html#module-datetime)
- [InfluxDB Client](https://github.com/influxdata/influxdb-python)
