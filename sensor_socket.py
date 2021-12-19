from tkinter import *
import tkinter as tk
import paho.mqtt.client as mqtt
import time
import random


class Sensor:
    def __init__(self, name, turn):
        self.name = name
        self.turn = turn  # 1 - ON, 0 - OFF
        self.avr_temp = 25
        self.avr_smoke = 5
        self.temperature = self.avr_temp + random.randint(-5, 5)
        self.smoke = self.avr_smoke + random.randint(-2, 2)

    def get_temperature(self):
        self.temperature = (self.avr_temp + random.randint(-5, 5) if self.turn == 1 else 0)
        return self.temperature

    def get_smoke(self):
        self.smoke = (self.avr_smoke + random.randint(-2, 2) if self.turn == 1 else 0)
        if self.smoke < 0:
            self.smoke = 0
        if self.smoke > 100:
            self.smoke = 100
        return self.smoke

    def sensor_turn(self, turn):
        self.turn = turn  # 1 - ON, 0 - OFF

    def publish_all(self, client):
        client.publish(self.name + '/turn', payload=str(self.turn))
        client.publish(self.name + '/temperature', self.get_temperature())
        client.publish(self.name + '/smoke', self.get_smoke())


sensors = {'sensor1': Sensor('sensor1', 1),
           'sensor2': Sensor('sensor2', 1),
           'sensor3': Sensor('sensor3', 1)}


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe('server/turn')
        for sensor in sensors:
            client.subscribe('server/turn_' + sensor)  # включение/отключение датчика
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    print(msg.topic + ' | ' + payload)
    name_sensor = topic.split('_')[-1]
    if 'server/turn_' in topic:
        sensors[name_sensor].sensor_turn(int(payload))
    elif topic == 'server/turn':
        print("CONNECT SERVER")

    test_on_message(topic, payload, name_sensor)


def test_on_message(topic, payload, name_sensor):
    if 'test' in topic:
        if 'test/avr_tmp_' in topic:
            sensors[name_sensor].avr_temp = int(payload)
        elif 'test/avr_smoke_' in topic:
            sensors[name_sensor].avr_smoke = int(payload)


def test_on_connect():
    for sensor in sensors:
        client.subscribe('test/avr_tmp_' + sensor)
        client.subscribe('test/avr_smoke_' + sensor)


if __name__ == '__main__':
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.on_message = on_message
    client.on_connect = on_connect
    test_on_connect()
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
