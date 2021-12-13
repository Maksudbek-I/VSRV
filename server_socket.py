from tkinter import *
import paho.mqtt.client as mqtt
import time

class Server_socket(mqtt.Client):
	def __init__(self):	
		self.name = 'server'

client_sockets = ['sensor1', 'sensor2', 'sensor3']


def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	for s in client_sockets:
		client.subscribe(s+'/turn')
		client.subscribe(s+'/temperature')
		client.subscribe(s+'/smoke')
		client.subscribe(s+'/power')


def on_message(client, userdata, msg):
	topic = msg.topic
	payload = msg.payload.decode('utf-8')
	print(msg.topic + '||' + payload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()