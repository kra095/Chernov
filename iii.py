import tkinter as tk
from tkinter import ttk, messagebox

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("600x400")

        # Поля выбора валют
        ttk.Label(root, text="Из:").grid(row=0, column=0, padx=5, pady=5)
        self.from_currency = ttk.Combobox(root, values=["USD", "EUR", "RUB", "GBP", "JPY"])
        self.from_currency.grid(row=0, column=1, padx=5, pady=5)
        self.from_currency.set("USD")

        ttk.Label(root, text="В:").grid(row=1, column=0, padx=5, pady=5)
        self.to_currency = ttk.Combobox(root, values=["USD", "EUR", "RUB", "GBP", "JPY"])
        self.to_currency.grid(row=1, column=1, padx=5, pady=5)
        self.to_currency.set("EUR")

        # Поле ввода суммы
        ttk.Label(root, text="Сумма:").grid(row=2, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка конвертации
        self.convert_button = ttk.Button(root, text="Конвертировать", command=self.convert)
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица истории
        self.history_tree = ttk.Treeview(root, columns=("From", "To", "Amount", "Result"), show="headings")
        self.history_tree.heading("From", text="Из")
        self.history_tree.heading("To", text="В")
        self.history_tree.heading("Amount", text="Сумма")
        self.history_tree.heading("Result", text="Результат")
        self.history_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    def convert(self):
        # Здесь будет логика конвертации
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
