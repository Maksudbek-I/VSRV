import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe('server/fire_alarm')
        client.subscribe('server/turn')  # включение/отключение датчика
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    print(msg.topic + ' | ' + payload)
    if 'server/fire_alarm' == topic:
        print("-----------------------------------")
        if payload == '1':
            print(" F I R E   A L A R M  :  S T A R T ")
        elif payload == '0':
            print("  F I R E   A L A R M  :  S T O P  ")
        print("-----------------------------------")
    elif topic == 'server/turn':
        print("CONNECT SERVER")


if __name__ == '__main__':
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.on_message = on_message
    client.on_connect = on_connect
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print('exiting')
        client.disconnect()
        client.loop_stop()
