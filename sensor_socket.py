from tkinter import *
import paho.mqtt.client as mqtt
import time
import random

class Sensor:
    def __init__(self, name, turn):
        self.name = name
        self.turn = turn
        self.temperature = random.randint(16, 100)
        self.smoke = random.randint(0, 100)

    def get_temperature(self):
            self.temperature = (random.randint(16, 100) if self.turn else 0)
            return self.temperature

    def get_smoke(self):
            self.smoke = (random.randint(0, 100) if self.turn else 0)
            return self.smoke

    def sensor_turn(self, turn):
            self.turn = turn

    def publish_all(self, client):
            client.publish(self.name+'/turned', payload=('ON' if self.turn else 'OFF'))
            client.publish(self.name+'/temperature', self.get_temperature())
            client.publish(self.name+'/smoke', self.get_smoke())


sensors = {'sensor1': Sensor('sensor1', True),
           'sensor2': Sensor('sensor2', True),
           'sensor3': Sensor('sensor3', True)}


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        for sensor in sensors:
            client.subscribe(sensor+'/turn') # включение/отключение датчика
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    print(msg.topic + ' || ' + payload)

    if '/turn' in topic and 'sensor' in topic:
        name_sensor = topic.split('/')[0]
        if payload == '1':
            sockets[name_sensor].sensor_turn(True)
            sockets[name_sensor].publish_all(client)
        elif payload == '0':
            sockets[name_sensor].sensor_turn(False)
            sockets[name_sensor].publish_all(client)


if __name__ == '__main__':
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.on_message = on_message
    client.on_connect = on_connect
    client.loop_start()

    try:
        while True:
            time.sleep(1)
            for s in sensors:
                time.sleep(0.5)
                sensors[s].publish_all(client)
    except KeyboardInterrupt:
        print('exiting')
        client.disconnect()
        client.loop_stop()
