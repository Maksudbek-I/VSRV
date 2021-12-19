from tkinter import *
import tkinter as tk
import paho.mqtt.client as mqtt
import time
import random


class sensor_management_block(tk.Frame):
    """
    Класс для отображения информации о датчике
    """

    def __init__(self, window, name):
        super().__init__(window, width=100, height=100, bg='#a7a7b8', padx=1, pady=1)
        self.turn = 0
        self.name = name

        # Имя датчика
        self.label_name = Label(self, text=self.name, fg="#000000", bg="#cfe1d4", width=15, height=2)
        self.label_name.grid(row=0, column=0)

        # Отображение показателей
        self.indicators = tk.Frame(self)
        self.temperature_label = Label(self.indicators, text=' avr temperature: ', fg="#000000", bg="#cfe1d4", width=15,
                                       height=2)
        self.smoke_label = Label(self.indicators, text='avr smoke: ', fg="#000000", bg="#cfe1d4", width=15, height=2)
        self.temperature_strvar = StringVar()
        self.smoke_strvar = StringVar()
        self.temperature_value = Entry(self.indicators, textvariable=self.temperature_strvar)
        self.smoke_value = Entry(self.indicators, textvariable=self.smoke_strvar)
        self.temperature_button = tk.Button(self.indicators, text="set", width=10, height=2)
        self.temperature_button['command'] = self.click_button_set_temp
        self.smoke_button = tk.Button(self.indicators, text="set", width=10, height=2)
        self.smoke_button['command'] = self.click_button_set_smoke

        self.temperature_button.grid(row=0, column=2)
        self.smoke_button.grid(row=1, column=2)
        self.temperature_label.grid(row=0, column=0)
        self.temperature_value.grid(row=0, column=1)
        self.smoke_label.grid(row=1, column=0)
        self.smoke_value.grid(row=1, column=1)
        self.indicators.grid(row=0, column=1)

    def click_button_set_temp(self):
        client.publish('test/avr_tmp_' + self.name, self.temperature_strvar.get())

    def click_button_set_smoke(self):
        client.publish('test/avr_smoke_' + self.name, self.smoke_strvar.get())


class sensor_management_app(tk.Tk):
    """
    Класс для графического управления средними показателями сенсоров (основное окно)
    """

    def __init__(self):
        super().__init__()
        self.title('Sensors')
        self.geometry('450x280')  # Размер

        # создание фрейма и отображение датчиков
        self.left_frame = Frame(self)
        self.sensor_mng = {'sensor1': sensor_management_block(self.left_frame, "sensor1"),
                           'sensor2': sensor_management_block(self.left_frame, "sensor2"),
                           'sensor3': sensor_management_block(self.left_frame, "sensor3")}

        self.sensor_mng['sensor1'].grid(row=0, column=0)
        self.sensor_mng['sensor2'].grid(row=1, column=0)
        self.sensor_mng['sensor3'].grid(row=2, column=0)
        self.left_frame.pack()


def on_connect(client, userdata, flags, rc):
    pass


def on_message(client, userdata, msg):
    pass


if __name__ == "__main__":
    app = sensor_management_app()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_start()
    app.mainloop()