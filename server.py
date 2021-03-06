from tkinter import *
import tkinter as tk
import paho.mqtt.client as mqtt
import time
import sqlite3
import datetime


class sensor_information_block(tk.Frame):
    """
    Класс для отображения информации о датчике
    """

    def __init__(self, window, name):
        super().__init__(window, width=100, height=100, bg='#a7a7b8', padx=1, pady=1)
        self.turn = 0
        self.name = name
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Имя датчика
        self.label_name = Label(self, text=self.name, fg="#000000", bg="#cfe1d4", width=15, height=2)
        self.label_name.grid(row=0, column=1)

        # Отображение состояния датчика
        self.connect_button = tk.Button(self, text="disconnect", fg="#eee", bg="#d2082d", width=10, height=2)
        self.connect_button['command'] = self.click_button_connect
        self.connect_button.grid(row=0, column=0)

        # Отображение показателей
        self.indicators = tk.Frame(self)
        self.temperature_label = Label(self.indicators, text='  temperature: ', fg="#000000", bg="#cfe1d4", width=10,
                                       height=2)
        self.smoke_label = Label(self.indicators, text='smoke: ', fg="#000000", bg="#cfe1d4", width=10, height=2)
        self.temperature_value = Label(self.indicators, text='0' + ' C', fg="#000000", bg="#cfe1d4", width=10, height=2)
        self.smoke_value = Label(self.indicators, text='0' + ' %', fg="#000000", bg="#cfe1d4", width=10, height=2)
        self.temperature_label.grid(row=0, column=0)
        self.temperature_value.grid(row=0, column=1)
        self.smoke_label.grid(row=1, column=0)
        self.smoke_value.grid(row=1, column=1)
        self.indicators.grid(row=0, column=2)

    def click_button_connect(self):
        if self.turn == 1:
            # disconnect
            client.publish("server/turn_" + self.name, '0')
            self.connect(0)
        else:
            client.publish("server/turn_" + self.name, '1')
            self.connect(0)

    def set_temperature(self, tmp):
        self.temperature_value['text'] = tmp + ' C'
        self.temperature_value.grid(row=0, column=1)

    def set_smoke(self, smk):
        self.smoke_value['text'] = smk + ' %'
        self.smoke_value.grid(row=1, column=1)

    def connect(self, flag):
        """
        Функция изменяет изображение информации о датчике
        flag == True - датчик подключен
        flag == False - датчик отключен
        """
        self.turn = flag
        if flag == 1:
            self.connect_button["text"] = "connect"
            self.connect_button["bg"] = "#00a51c"
        else:
            self.connect_button["text"] = "disconnect"
            self.connect_button["bg"] = "#d2082d"


class App(tk.Tk):
    """
    Класс для отображения информации о сервере (основное окно)
    """

    def __init__(self):
        super().__init__()
        self.title('Server')
        self.geometry('350x450')  # Размер
        self.left_frame = Frame(self, bg='#9898ff')
        self.client_sockets = {'sensor1': sensor_information_block(self.left_frame, "sensor1"),
                               'sensor2': sensor_information_block(self.left_frame, "sensor2"),
                               'sensor3': sensor_information_block(self.left_frame, "sensor3")}

        self.client_sockets['sensor1'].grid(row=0, column=0)
        self.client_sockets['sensor2'].grid(row=1, column=0)
        self.client_sockets['sensor3'].grid(row=2, column=0)
        self.left_frame.grid(row=0, column=0, sticky="nesw")

        self.right_frame = Frame(self, bg="#ddddff")
        self.fire_alarm_label = Label(self.right_frame, text='Fire alarm system', fg="#000000", bg="#cfe1d4", width=20,
                                      height=5)
        self.fire_alarm_status_label = Label(self.right_frame, text='status: OFF', fg="#000000", bg="#00a51c", width=20,
                                             height=5)
        self.fire_alarm_label.grid(row=0, column=0)
        self.fire_alarm_status_label.grid(row=1, column=0)
        self.right_frame.grid(row=1, column=0, sticky="nesw")

    def turn_sensor(self, name_sensor, turn):
        self.client_sockets[name_sensor].connect(turn)

    def set_fire_alarm_status(self, status):
        if status == 1:
            self.fire_alarm_status_label["text"] = 'status: ON'
            self.fire_alarm_status_label["bg"] = "#00a51c"
        elif status == 0:
            self.fire_alarm_status_label["text"] = 'status: OFF'
            self.fire_alarm_status_label["bg"] = "#d2082d"


def stop():
    app.client.disconnect()
    app.client.loop_stop()


def on_connect(client, userdata, flags, rc):
    for s in app.client_sockets:
        client.subscribe(s + '/turn')
        client.subscribe(s + '/temperature')
        client.subscribe(s + '/smoke')


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    add_logs(topic, payload)
    if 'sensor' in topic:
        name_sensor = topic.split('/')[0]
        if 'temperature' in topic:
            app.client_sockets[name_sensor].set_temperature(payload)
        elif 'smoke' in topic:
            app.client_sockets[name_sensor].set_smoke(payload)
        elif 'turn' in topic:
            app.client_sockets[name_sensor].connect(int(payload))
    check()


def add_logs(topic, payload):
    data_tuple = (topic, payload, datetime.datetime.now())
    comm = """INSERT INTO 'logs' VALUES (?, ?, ?);"""
    cursor.execute(comm, data_tuple)
    conn.commit()


def create_table():
    try:
        cursor.execute("""CREATE TABLE logs
		(topic TEXT NOT NULL,
		payload TEXT NOT NULL,
		joiningDate timestamp)
		""")
    except:
        # таблица уже создана
        pass


FIRE = 0


def check():
    status = False
    global FIRE
    for s in app.client_sockets:
        if int(app.client_sockets[s].temperature_value['text'].split()[0]) >= 60:
            status = True
        if int(app.client_sockets[s].smoke_value['text'].split()[0]) >= 30:
            status = True
    if status and FIRE != 1:
        FIRE = 1
        app.set_fire_alarm_status(1)
        client.publish('server/fire_alarm', '1')
    elif not status and FIRE != 0:
        FIRE = 0
        app.set_fire_alarm_status(0)
        client.publish('server/fire_alarm', '0')


if __name__ == "__main__":
    conn = sqlite3.connect("logs.db", check_same_thread=False)
    cursor = conn.cursor()
    create_table()
    app = App()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)

    client.publish('server/turn', '1')
    client.loop_start()
    app.mainloop()
