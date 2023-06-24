import tkinter as tk
import re
import sqlite3
from tkinter import messagebox
from tkinter import filedialog
import os

def sort_by_ip():
    filename = 'access_logs.log'
    sorted_lines = []

    with open(filename, 'r') as file:
        lines = file.readlines()
        sorted_lines = sorted(lines, key=extract_ip)

    sorted_filename = 'sorted_by_ip.log'
    with open(sorted_filename, 'w') as sorted_file:
        sorted_file.writelines(sorted_lines)

    print("Лог-файл отсортирован по IP-адресам и сохранен в файл:", sorted_filename)
    save_to_database(sorted_lines)

def sort_by_query():
    query = entry_query.get()
    filename = 'access_logs.log'
    sorted_lines = []

    with open(filename, 'r') as file:
        lines = file.readlines()
        sorted_lines = [line for line in lines if query in line]

    sorted_filename = 'sorted_by_query.log'
    with open(sorted_filename, 'w') as sorted_file:
        sorted_file.writelines(sorted_lines)

    print("Лог-файл отсортирован по запросу и сохранен в файл:", sorted_filename)
    save_to_database(sorted_lines)

def extract_ip(line):
    ip_match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
    if ip_match:
        return ip_match.group()
    return ""

def save_to_database(lines):
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()

    # Создание таблицы, если она не существует
    c.execute('''CREATE TABLE IF NOT EXISTS sorted_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, line TEXT)''')

    # Вставка отсортированных строк в таблицу
    for line in lines:
        c.execute("INSERT INTO sorted_logs (line) VALUES (?)", (line,))

    conn.commit()
    conn.close()

def open_database():
    filepath = filedialog.askopenfilename(filetypes=[('SQLite Databases', '*.db')])
    if filepath:
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()

        # Получение информации о таблицах в базе данных
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        table_info = ""
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table[0]});")
            columns = cursor.fetchall()

            table_info += f"\nТаблица: {table[0]}\n"
            table_info += "---------------------------------\n"
            for column in columns:
                table_info += f"Название столбца: {column[1]}\n"
                table_info += f"Тип данных: {column[2]}\n"
                table_info += "---------------------------------\n"

        messagebox.showinfo("Информация о базе данных", f"База данных: {filepath}\n\n{table_info}")

        conn.close()

def delete_database():
    filepath = filedialog.askopenfilename(filetypes=[('SQLite Databases', '*.db')])
    if filepath:
        try:
            os.remove(filepath)
            messagebox.showinfo("Удаление базы данных", f"База данных успешно удалена: {filepath}")
        except Exception as e:
            messagebox.showerror("Ошибка удаления базы данных", str(e))

root = tk.Tk()

label_query = tk.Label(root, text="Запрос:")
label_query.pack()

entry_query = tk.Entry(root)
entry_query.pack()

btn_sort_ip = tk.Button(root, text="Сортировать по IP-адресам", command=sort_by_ip)
btn_sort_ip.pack()

btn_sort_query = tk.Button(root, text="Сортировать по запросу", command=sort_by_query)
btn_sort_query.pack()

btn_open_database = tk.Button(root, text="Открыть базу данных", command=open_database)
btn_open_database.pack()

btn_delete_database = tk.Button(root, text="Удалить базу данных", command=delete_database)
btn_delete_database.pack()

root.mainloop()