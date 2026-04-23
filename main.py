import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = 'training_data.json'

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        
        # Поля ввода
        self.create_input_fields()
        
        # Таблица
        self.create_table()
        
        # Загружаем данные
        self.training_data = []
        self.load_data()

        # Фильтры
        self.create_filters()

        # Обновляем таблицу
        self.update_table()

        # Обработчик закрытия
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_input_fields(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, padx=5)
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Тип тренировки:").grid(row=0, column=2, padx=5)
        self.type_entry = ttk.Entry(frame)
        self.type_entry.grid(row=0, column=3, padx=5)

        ttk.Label(frame, text="Длительность (мин):").grid(row=0, column=4, padx=5)
        self.duration_entry = ttk.Entry(frame)
        self.duration_entry.grid(row=0, column=5, padx=5)

        add_button = ttk.Button(frame, text="Добавить тренировку", command=self.add_training)
        add_button.grid(row=0, column=6, padx=5)

    def create_table(self):
        columns = ('date', 'type', 'duration')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.tree.heading('date', text='Дата')
        self.tree.heading('type', text='Тип тренировки')
        self.tree.heading('duration', text='Длительность')
        self.tree.pack(pady=10)

    def create_filters(self):
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=10)

        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0, padx=5)
        self.filter_type = ttk.Entry(filter_frame)
        self.filter_type.grid(row=0, column=1, padx=5)
        self.filter_type.bind("<KeyRelease>", lambda e: self.update_table())

        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=2, padx=5)
        self.filter_date = ttk.Entry(filter_frame)
        self.filter_date.grid(row=0, column=3, padx=5)
        self.filter_date.bind("<KeyRelease>", lambda e: self.update_table())

    def add_training(self):
        date_str = self.date_entry.get()
        t_type = self.type_entry.get()
        duration_str = self.duration_entry.get()

        # Проверка данных
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты")
            return

        if not t_type:
            messagebox.showerror("Ошибка", "Введите тип тренировки")
            return

        try:
            duration = int(duration_str)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return

        record = {
            'date': date_str,
            'type': t_type,
            'duration': duration
        }
        self.training_data.append(record)
        self.update_table()
        self.clear_entries()

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def update_table(self):
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)

        filtered_data = self.training_data

        filter_type = self.filter_type.get().lower()
        filter_date = self.filter_date.get()

        if filter_type:
            filtered_data = [d for d in filtered_data if filter_type in d['type'].lower()]

        if filter_date:
            filtered_data = [d for d in filtered_data if d['date'] == filter_date]

        for item in filtered_data:
            self.tree.insert('', tk.END, values=(item['date'], item['type'], item['duration']))

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.training_data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                self.training_data = json.load(f)

    def on_close(self):
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
