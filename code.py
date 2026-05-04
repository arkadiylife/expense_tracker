import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

DATA_FILE = "expenses.json"

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x500")

        # Загрузка данных
        self.expenses = self.load_expenses()

        # Создание виджетов
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # Поля ввода
        ttk.Label(self.root, text="Сумма:").grid(row=0, column=0, padx=10, pady=10)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.root, text="Категория:").grid(row=0, column=2, padx=10, pady=10)
        self.category_entry = ttk.Entry(self.root)
        self.category_entry.grid(row=0, column=3, padx=10, pady=10)

        ttk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4, padx=10, pady=10)
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=0, column=5, padx=10, pady=10)

        # Кнопка добавления
        ttk.Button(self.root, text="Добавить расход", command=self.add_expense).grid(
            row=0, column=6, padx=10, pady=10)

        # Таблица расходов
        self.tree = ttk.Treeview(self.root, columns=("amount", "category", "date"), show="headings")
        self.tree.heading("amount", text="Сумма")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")
        self.tree.grid(row=1, column=0, columnspan=7, padx=10, pady=10, sticky="nsew")

        # Фильтры и выбор периода
        ttk.Label(self.root, text="Фильтр по категории:").grid(row=2, column=0, padx=10, pady=5)
        self.filter_category = ttk.Combobox(self.root, values=self.get_unique_categories())
        self.filter_category.grid(row=2, column=1, padx=10, pady=5)
        ttk.Button(self.root, text="Фильтровать", command=self.filter_expenses).grid(
            row=2, column=2, padx=10, pady=5)

        ttk.Label(self.root, text="Период с:").grid(row=2, column=3, padx=10, pady=5)
        self.start_date_entry = ttk.Entry(self.root)
        self.start_date_entry.grid(row=2, column=4, padx=10, pady=5)

        ttk.Label(self.root, text="по:").grid(row=2, column=5, padx=10, pady=5)
        self.end_date_entry = ttk.Entry(self.root)
        self.end_date_entry.grid(row=2, column=6, padx=10, pady=5)

        ttk.Button(self.root, text="Сумма за период", command=self.sum_for_period).grid(
            row=2, column=7, padx=10, pady=5)

    def load_expenses(self):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_expenses(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.expenses, f, indent=4)

    def get_unique_categories(self):
        return list({exp["category"] for exp in self.expenses})
    def validate_input(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        if not amount.replace(".", "", 1).isdigit() or float(amount) <= 0:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом.")
            return False

        if not category:
            messagebox.showerror("Ошибка", "Введите категорию.")
            return False

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД.")
            return False

        return True

    def add_expense(self):
        if not self.validate_input():
            return

        expense = {
            "amount": float(self.amount_entry.get()),
            "category": self.category_entry.get(),
            "date": self.date_entry.get()
        }

        self.expenses.append(expense)
        self.save_expenses()
        self.update_table()

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for exp in self.expenses:
            self.tree.insert("", "end", values=(exp["amount"], exp["category"], exp["date"]))


    def filter_expenses(self):
        category = self.filter_category.get()
        filtered = [exp for exp in self.expenses if exp["category"] == category]
        
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for exp in filtered:
            self.tree.insert("", "end", values=(exp["amount"], exp["category"], exp["date"]))

    def sum_for_period(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            if start > end:
                messagebox.showerror("Ошибка", "Дата начала не может быть позже даты окончания.")
                return

            total = sum(
                exp["amount"] for exp in self.expenses 
                if start <= datetime.strptime(exp["date"], "%Y-%m-%d") <= end
            )
            
            messagebox.showinfo("Сумма за период", f"Итого: {total:.2f} руб.")
        
        except ValueError:
            messagebox.showerror("Ошибка", "Введите даты в формате ГГГГ-ММ-ДД.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
