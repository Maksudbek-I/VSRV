import sqlite3, datetime

sqlite_connection = sqlite3.connect('logs.db')
cursor = sqlite_connection.cursor()
print("Подключен к SQLite")

cursor = sqlite_connection.cursor()
# получить данные разработчика
sqlite_select_query = """SELECT * from logs"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
for row in records:
	print(row)

cursor.close()
