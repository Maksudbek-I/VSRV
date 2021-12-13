from tkinter import *
import tkinter as tk

class sensor_information_block(tk.Frame):
	"""
	Класс для отображения информации о датчике
	"""
	def __init__(self, window, name):	
		super().__init__(window, width=100, height=100, bg='#a7a7b8', padx=1, pady=1)
		self.grid_columnconfigure(0, weight = 5)
		self.grid_columnconfigure(1, weight = 2)
		self.grid_rowconfigure(0, weight = 1)

		# Имя датчика
		self.label = Label(self, text=name, fg="#000000", bg="#cfe1d4", width=15, height=2) 
		self.label.grid(row=0, column=0)

		# Отображение состояния датчика
		self.connect_label = Label(self, text="disconnect", fg="#eee", bg="#d2082d", width=10, height=2)
		self.connect_label.grid(row=0, column=1)

	def connect(self, flag):
		"""
		Функция изменяет изображение информации о датчике
		flag == True - датчик подключен
		flag == False - датчик отключен
		"""
		if flag:
			self.connect_label["text"] = "connect"
			self.connect_label["bg"] = "#00a51c"
		else:
			self.connect_label["text"] = "disconnect"
			self.connect_label["bg"] = "#d2082d"


class App(tk.Tk):
	"""
	Класс для отображения информации о сервере (основное окно)
	"""
	def __init__(self):
		super().__init__()
		self.title('Server')
		self.geometry('900x450')#Размер
		self.grid_columnconfigure(0, weight = 3)
		self.grid_columnconfigure(1, weight = 5)
		self.grid_rowconfigure(0, weight = 1)

		# создание фрейма и отображение датчиков
		left_frame = Frame(self, bg='#9898ff')
		sib1 = sensor_information_block(left_frame, "sib1")
		sib1.grid(row=0, column=0)
		sib2 = sensor_information_block(left_frame, "sib2")
		sib2.grid(row=1, column=0)
		sib2.connect(True)
		sib3 = sensor_information_block(left_frame, "sib3")
		sib3.grid(row=2, column=0)
		sib4 = sensor_information_block(left_frame, "sib4")
		sib4.grid(row=3, column=0)
		left_frame.grid(row = 0, column = 0, sticky = "nesw")

		right_frame = Frame(self, bg = "#ddddff")
		right_frame.grid(row = 0, column = 1, sticky = "nesw")


if __name__ == "__main__":
	app = App()
	app.mainloop()