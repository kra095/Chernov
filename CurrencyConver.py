import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("700x500")

        # Поля выбора валют
        ttk.Label(root, text="Из:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.from_currency = ttk.Combobox(root, values=["USD", "EUR", "RUB", "GBP", "JPY", "CNY"])
        self.from_currency.grid(row=0, column=1, padx=10, pady=10)
        self.from_currency.set("USD")

        ttk.Label(root, text="В:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.to_currency = ttk.Combobox(root, values=["USD", "EUR", "RUB", "GBP", "JPY", "CNY"])
        self.to_currency.grid(row=1, column=1, padx=10, pady=10)
        self.to_currency.set("EUR")

        # Поле ввода суммы
        ttk.Label(root, text="Сумма:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10)

        # Кнопка конвертации
        self.convert_button = ttk.Button(root, text="Конвертировать", command=self.convert)
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Таблица истории
        columns = ("From", "To", "Amount", "Result", "Rate")
        self.history_tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=120)

        self.history_tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Полосы прокрутки для таблицы
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.history_tree.yview)
        scrollbar.grid(row=4, column=2, sticky="ns")
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        # Загрузка истории при запуске
        self.load_history()

    def get_exchange_rate(self, from_curr, to_curr):
        api_key = "YOUR_API_KEY_HERE"  # Замените на ваш API-ключ
        url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка на HTTP-ошибки
            data = response.json()

            if to_curr in data["rates"]:
                return data["rates"][to_curr]
            else:
                raise ValueError(f"Валюта {to_curr} не найдена в API")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка сети", f"Не удалось подключиться к API: {e}")
            return None
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении курса: {e}")
            return None

    def convert(self):
        try:
            # Проверка ввода суммы
            amount_str = self.amount_entry.get().strip()
            if not amount_str:
                messagebox.showerror("Ошибка", "Введите сумму для конвертации")
                return

            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
                return

            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()

            if not from_curr or not to_curr:
                messagebox.showerror("Ошибка", "Выберите валюты для конвертации")
                return

            # Получение курса
            rate = self.get_exchange_rate(from_curr, to_curr)
            if rate is None:
                return

            # Расчёт результата
            result = amount * rate

            # Добавление в историю
            self.add_to_history(from_curr, to_curr, amount, result, rate)

            # Отображение результата
            messagebox.showinfo(
                "Результат конвертации",
                f"{amount:.2f} {from_curr} = {result:.2f} {to_curr}\n"
                f"Курс: 1 {from_curr} = {rate:.4f} {to_curr}"
            )

        except ValueError:
            messagebox.showerror("Ошибка ввода", "Введите корректное число в поле суммы")
        except Exception as e:
            messagebox.showerror("Неожиданная ошибка", f"Произошла ошибка: {e}")

    def load_history(self):
        """Загрузка истории из JSON-файла"""
        if os.path.exists("history.json"):
            try:
                with open("history.json", "r", encoding="utf-8") as f:
                    history = json.load(f)
                    # Очистка таблицы перед загрузкой
                    for item in self.history_tree.get_children():
                        self.history_tree.delete(item)
                    # Заполнение таблицы
                    for record in history:
                        self.history_tree.insert("", "end", values=(
                            record["from"],
                            record["to"],
                            f"{record['amount']:.2f}",
                            f"{record['result']:.2f}",
                            f"{record['rate']:.4f}"
                ))
            except (json.JSONDecodeError, IOError) as e:
                messagebox.showwarning("Предупреждение", f"Не удалось загрузить историю: {e}")

    def save_history(self, history):
        """Сохранение истории в JSON-файл"""
        try:
            with open("history.json", "w", encoding="utf-8") as f:
                json.dump(history, f, indent=4, ensure_ascii=False)
        except IOError as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить историю: {e}")

    def add_to_history(self, from_curr, to_curr, amount, result, rate):
        """Добавление записи в историю"""
        history = self.load_history_file()
        history.append({
            "from": from_curr,
            "to": to_curr,
            "amount": amount,
            "result": result,
            "rate": rate,
            "timestamp": self.get_current_time()
        })
        self.save_history(history)
        # Обновляем отображение таблицы
        self.load_history()

    def load_history_file(self):
        """Вспомогательная функция для загрузки истории как списка"""
        if os.path.exists("history.json"):
            try:
                with open("history.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    @staticmethod
    def get_current_time():
        """Получение текущей даты и времени"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
