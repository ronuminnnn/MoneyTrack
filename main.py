import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from tkinter import messagebox
from database import (
    add_transaction,
    create_table,
    get_transactions,
    delete_transaction,
    get_balance,
    get_financial_summary,
    get_expenses_by_category,
    set_monthly_budget,
    get_monthly_budget,
    get_monthly_expenses,
    get_transaction_by_id,
    update_transaction
)
from datetime import datetime
import sqlite3

# Настройки внешнего вида
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class MoneyTrackApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Настройки окна
        self.title("MoneyTrack — Учёт финансов")
        self.geometry("1100x700")
        self.minsize(800, 550)

        # Цвета приложения
        self.bg_color = "#15151F"
        self.sidebar_color = "#1E1E2D"
        self.accent_color = "#8B5CF6"
        self.text_color = "#FFFFFF"

        self.configure(fg_color=self.bg_color)

        # Основная сетка
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Объявляем боковое меню
        self.sidebar = None

        # Создание бокового меню
        self.create_sidebar()

        # Область содержимого
        self.content = ctk.CTkFrame(
            self,
            fg_color=self.bg_color,
            corner_radius=0
        )

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=20,
            pady=20
        )

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        # Открываем главный экран
        self.show_page("Главная")

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=200,
            corner_radius=0,
            fg_color=self.sidebar_color
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # Название приложения
        logo = ctk.CTkLabel(
            self.sidebar,
            text="MoneyTrack",
            font=("Arial", 25, "bold"),
            text_color=self.accent_color
        )

        logo.pack(pady=(30, 10))

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Управляй своими финансами",
            font=("Arial", 11),
            text_color="#A0A0B0"
        )

        subtitle.pack(pady=(0, 35))

        # Кнопки навигации
        pages = [
            "Главная",
            "Операции",
            "Добавить операцию",
            "Статистика",
            "Настройки"
        ]

        for page in pages:

            button = ctk.CTkButton(
                self.sidebar,
                text=page,
                height=45,
                corner_radius=10,
                fg_color="transparent",
                hover_color="#35354A",
                text_color=self.text_color,
                anchor="w",
                font=("Arial", 14),
                command=lambda p=page: self.show_page(p)
            )

            button.pack(
                fill="x",
                padx=15,
                pady=5
            )

        # Нижняя подпись
        footer = ctk.CTkLabel(
            self.sidebar,
            text="MoneyTrack v1.0",
            text_color="#777788",
            font=("Arial", 11)
        )

        footer.pack(side="bottom", pady=20)

    def show_page(self, page_name):

        # Очищаем предыдущий экран
        for widget in self.content.winfo_children():
            widget.destroy()

        # Заголовок страницы
        title = ctk.CTkLabel(
            self.content,
            text=page_name,
            font=("Arial", 28, "bold"),
            text_color=self.text_color
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(10, 25)
        )

        # Вывод содержимого страницы
        if page_name == "Главная":
            self.show_dashboard()

        elif page_name == "Операции":
            self.show_transactions()

        elif page_name == "Добавить операцию":
            self.show_add_transaction()

        elif page_name == "Статистика":
            self.show_statistics()

        elif page_name == "Настройки":
            self.show_settings()

    def show_dashboard(self):

        # Приветствие
        welcome = ctk.CTkLabel(
            self.content,
            text="Добро пожаловать в MoneyTrack!",
            font=("Arial", 20, "bold")
        )

        welcome.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 20)
        )

        # Контейнер карточек
        cards_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        cards_frame.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        for column in range(3):
            cards_frame.grid_columnconfigure(column, weight=1)

        # Данные карточек пока демонстрационные
        # Получаем реальные финансовые данные
        balance = get_balance()
        income, expenses = get_financial_summary()

        # Карточки с актуальными данными
        cards = [
            ("Текущий баланс", f"{balance:.2f} ₽", "#8B5CF6"),
            ("Доходы", f"{income:.2f} ₽", "#22C55E"),
            ("Расходы", f"{expenses:.2f} ₽", "#EF4444")
        ]

        for index, (name, value, color) in enumerate(cards):
            card = ctk.CTkFrame(
                cards_frame,
                fg_color="#242436",
                corner_radius=15,
                height=130
            )

            card.grid_columnconfigure(0, weight=1)

            card.grid(
                row=0,
                column=index,
                padx=7,
                sticky="ew"
            )

            card.grid_propagate(False)

            label = ctk.CTkLabel(
                card,
                text=name,
                font=("Arial", 13),
                text_color="#B0B0C0"
            )

            label.pack(
                anchor="w",
                padx=15,
                pady=(20, 10)
            )

            amount = ctk.CTkLabel(
                card,
                text=value,
                font=("Arial", 24, "bold"),
                text_color=color
            )

            amount.pack(anchor="w", padx=15)

        # Последние операции
        recent_title = ctk.CTkLabel(
            self.content,
            text="Последние операции",
            font=("Arial", 19, "bold")
        )

        recent_title.grid(
            row=3,
            column=0,
            sticky="w",
            pady=(35, 15)
        )

        # Получаем последние операции
        transactions = get_transactions()[:5]

        if not transactions:
            empty_text = ctk.CTkLabel(
                self.content,
                text="Пока операций нет. Добавьте первую операцию!",
                font=("Arial", 14),
                text_color="#9090A0"
            )
            empty_text.grid(
                row=4,
                column=0,
                sticky="w"
            )

        else:
            for index, transaction in enumerate(transactions):
                transaction_id, transaction_type, amount, category, description, date = transaction

                color = (
                    "#22C55E"
                    if transaction_type == "Доход"
                    else "#EF4444"
                )

                operation_frame = ctk.CTkFrame(
                    self.content,
                    fg_color="#242436",
                    corner_radius=10
                )

                operation_frame.grid(
                    row=index + 4,
                    column=0,
                    sticky="ew",
                    pady=5
                )

                operation_frame.grid_columnconfigure(0, weight=1)

                operation_label = ctk.CTkLabel(
                    operation_frame,
                    text=f"{date} | {category} | {description or 'Без описания'}",
                    font=("Arial", 13),
                    text_color="white"
                )

                operation_label.grid(
                    row=0,
                    column=0,
                    sticky="w",
                    padx=15,
                    pady=12
                )

                amount_label = ctk.CTkLabel(
                    operation_frame,
                    text=f"{'+' if transaction_type == 'Доход' else '-'}{amount:.2f} ₽",
                    font=("Arial", 14, "bold"),
                    text_color=color
                )

                amount_label.grid(
                    row=0,
                    column=1,
                    padx=15,
                    pady=12
                )

    def show_placeholder(self, message):

        label = ctk.CTkLabel(
            self.content,
            text=message,
            font=("Arial", 15),
            text_color="#A0A0B0"
        )

        label.grid(
            row=1,
            column=0,
            sticky="nw"
        )

    def show_statistics(self):
        expenses = get_expenses_by_category()

        if not expenses:
            empty_label = ctk.CTkLabel(
                self.content,
                text="Пока нет расходов для отображения статистики.",
                font=("Arial", 15),
                text_color="#A0A0B0"
            )
            empty_label.grid(row=1, column=0, pady=30)
            return

        # Получаем категории и суммы
        categories = [item[0] for item in expenses]
        amounts = [item[1] for item in expenses]

        # Создаём диаграмму
        figure, axis = plt.subplots(figsize=(7, 5))

        axis.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%",
            startangle=90,
            textprops={
                "color": "white",
                "fontsize": 11
            }
        )

        axis.set_title(
            "Расходы по категориям",
            color="white",
            fontsize=15
        )

        figure.patch.set_facecolor("#15151F")
        axis.set_facecolor("#15151F")

        canvas = FigureCanvasTkAgg(figure, master=self.content)
        canvas.draw()
        canvas.get_tk_widget().grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        plt.close(figure)

        # Заголовок списка
        list_title = ctk.CTkLabel(
            self.content,
            text="Расходы по категориям",
            font=("Arial", 18, "bold"),
            text_color="white"
        )
        list_title.grid(row=2, column=0, pady=(20, 10))

        # Выводим категории и суммы
        for index, (category, amount) in enumerate(expenses):
            category_label = ctk.CTkLabel(
                self.content,
                text=f"{category}: {amount:.2f} ₽",
                font=("Arial", 14),
                text_color="#D1D1E0"
            )
            category_label.grid(
                row=index + 3,
                column=0,
                pady=5
            )

    def show_transactions(self):

        # Получаем операции из базы данных
        transactions = get_transactions()

        # Создаём прокручиваемую область
        transactions_frame = ctk.CTkScrollableFrame(
            self.content,
            fg_color="transparent"
        )

        transactions_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        # Если операций нет
        if not transactions:
            empty_label = ctk.CTkLabel(
                transactions_frame,
                text="Операций пока нет",
                font=("Arial", 16),
                text_color="#A0A0B0"
            )

            empty_label.pack(pady=30)
            return

        # Заголовок таблицы
        header = ctk.CTkFrame(
            transactions_frame,
            fg_color="#35354A",
            corner_radius=10
        )

        header.pack(fill="x", pady=5)

        columns = [
            "Дата",
            "Тип",
            "Категория",
            "Описание",
            "Сумма"
        ]

        for column, name in enumerate(columns):
            label = ctk.CTkLabel(
                header,
                text=name,
                font=("Arial", 12, "bold")
            )

            label.grid(
                row=0,
                column=column,
                padx=10,
                pady=12,
                sticky="w"
            )

        # Вывод каждой операции
        for transaction in transactions:

            transaction_id, transaction_type, amount, category, description, date = transaction

            row = ctk.CTkFrame(
                transactions_frame,
                fg_color="#242436",
                corner_radius=10
            )

            row.pack(fill="x", pady=4)

            values = [
                date,
                transaction_type,
                category,
                description or "Без описания",
                f"{amount:.2f} ₽"
            ]

            color = (
                "#22C55E"
                if transaction_type == "Доход"
                else "#EF4444"
            )


            for column, value in enumerate(values):
                label = ctk.CTkLabel(
                    row,
                    text=str(value),
                    font=("Arial", 12),
                    text_color=(
                        color if column == 4 else "#FFFFFF"
                    )
                )

                label.grid(
                    row=0,
                    column=column,
                    padx=10,
                    pady=12,
                    sticky="w"
                )
            delete_button = ctk.CTkButton(
                row,
                text="Удалить",
                width=80,
                fg_color="#EF4444",
                hover_color="#DC2626",
                command=lambda tid=transaction_id: self.delete_operation(tid)
            )

            delete_button.grid(
                row=0,
                column=5,
                padx=10,
                pady=12
            )

            edit_button = ctk.CTkButton(
                row,
                text="Изменить",
                width=80,
                fg_color="#8B5CF6",
                hover_color="#7041D8",
                command=lambda tid=transaction_id: self.edit_operation(tid)
            )

            edit_button.grid(
                row=0,
                column=6,
                padx=10,
                pady=12
            )


    def show_add_transaction(self):

        # Контейнер формы
        form = ctk.CTkFrame(
            self.content,
            fg_color="#242436",
            corner_radius=15
        )

        form.grid(
            row=1,
            column=0,
            sticky="new",
            padx=10,
            pady=10
        )

        # Настройка ширины формы
        form.grid_columnconfigure(0, weight=1)

        # Тип операции
        ctk.CTkLabel(
            form,
            text="Тип операции",
            font=("Arial", 14, "bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))

        self.type_menu = ctk.CTkOptionMenu(
            form,
            values=["Расход", "Доход"],
            width=300
        )
        self.type_menu.grid(row=1, column=0, sticky="w", padx=20, pady=5)

        # Сумма
        ctk.CTkLabel(
            form,
            text="Сумма",
            font=("Arial", 14, "bold")
        ).grid(row=2, column=0, sticky="w", padx=20, pady=(15, 5))

        self.amount_entry = ctk.CTkEntry(
            form,
            placeholder_text="Например, 1500",
            width=300
        )
        self.amount_entry.grid(row=3, column=0, sticky="w", padx=20, pady=5)

        # Категория
        ctk.CTkLabel(
            form,
            text="Категория",
            font=("Arial", 14, "bold")
        ).grid(row=4, column=0, sticky="w", padx=20, pady=(15, 5))

        self.category_menu = ctk.CTkOptionMenu(
            form,
            values=[
                "Продукты",
                "Транспорт",
                "Развлечения",
                "Здоровье",
                "Одежда",
                "Зарплата",
                "Подработка",
                "Подарки",
                "Другое"
            ],
            width=300
        )
        self.category_menu.grid(row=5, column=0, sticky="w", padx=20, pady=5)

        # Описание
        ctk.CTkLabel(
            form,
            text="Описание",
            font=("Arial", 14, "bold")
        ).grid(row=6, column=0, sticky="w", padx=20, pady=(15, 5))

        self.description_entry = ctk.CTkEntry(
            form,
            placeholder_text="Например, покупка продуктов",
            width=300
        )
        self.description_entry.grid(row=7, column=0, sticky="w", padx=20, pady=5)

        # Дата
        ctk.CTkLabel(
            form,
            text="Дата",
            font=("Arial", 14, "bold")
        ).grid(row=8, column=0, sticky="w", padx=20, pady=(15, 5))

        self.date_entry = ctk.CTkEntry(
            form,
            width=300
        )
        self.date_entry.grid(row=9, column=0, sticky="w", padx=20, pady=5)

        self.date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        # Кнопка сохранения
        save_button = ctk.CTkButton(
            form,
            text="Сохранить операцию",
            height=45,
            width=300,
            fg_color="#8B5CF6",
            hover_color="#7041D8",
            command=self.save_transaction
        )

        save_button.grid(
            row=10,
            column=0,
            padx=20,
            pady=25,
            sticky="w"
        )

        # Сообщения об ошибках и успешном сохранении
        self.form_message = ctk.CTkLabel(
            form,
            text="",
            font=("Arial", 13)
        )

        self.form_message.grid(
            row=11,
            column=0,
            padx=20,
            pady=(0, 15),
            sticky="w"
        )


    def save_transaction(self):

        # Получаем данные из формы
        transaction_type = self.type_menu.get()
        amount_text = self.amount_entry.get().strip()
        category = self.category_menu.get()
        description = self.description_entry.get().strip()
        date = self.date_entry.get().strip()

        # Проверяем сумму
        try:
            amount = float(amount_text.replace(",", "."))

            if amount <= 0:
                raise ValueError

        except ValueError:
            self.form_message.configure(
                text="Введите корректную сумму больше нуля!",
                text_color="#EF4444"
            )
            return

        # Проверяем дату
        try:
            datetime.strptime(date, "%Y-%m-%d")

        except ValueError:
            self.form_message.configure(
                text="Введите дату в формате ГГГГ-ММ-ДД!",
                text_color="#EF4444"
            )
            return

        # Сохраняем операцию в базу данных
        try:
            add_transaction(
                transaction_type,
                amount,
                category,
                description,
                date
            )

            self.form_message.configure(
                text="Операция успешно сохранена!",
                text_color="#22C55E"
            )

            # Очищаем поля после сохранения
            self.amount_entry.delete(0, "end")
            self.description_entry.delete(0, "end")

        except sqlite3.Error:
            self.form_message.configure(
                text="Ошибка при сохранении операции!",
                text_color="#EF4444"
            )
        except Exception as error:
            self.form_message.configure(
                text="Произошла непредвиденная ошибка!",
                text_color="#EF4444"
            )
            print("Ошибка:", error)

    def delete_operation(self, transaction_id):
        answer = messagebox.askyesno(
            "Удаление операции",
            "Ты действительно хочешь удалить эту операцию?"
        )

        if answer:
            delete_transaction(transaction_id)
            self.show_transactions()

    def edit_operation(self, transaction_id):
        transaction = get_transaction_by_id(transaction_id)

        if not transaction:
            messagebox.showerror("Ошибка", "Операция не найдена.")
            return

        # Получаем данные операции
        _, transaction_type, amount, category, description, date = transaction

        # Создаём окно редактирования
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Редактирование операции")
        edit_window.geometry("450x550")
        edit_window.resizable(False, False)
        edit_window.grab_set()

        # Заголовок
        ctk.CTkLabel(
            edit_window,
            text="Изменить операцию",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        # Тип операции
        ctk.CTkLabel(edit_window, text="Тип операции").pack(pady=5)

        type_menu = ctk.CTkOptionMenu(
            edit_window,
            values=["Расход", "Доход"],
            width=300
        )
        type_menu.pack(pady=5)
        type_menu.set(transaction_type)

        # Сумма
        ctk.CTkLabel(edit_window, text="Сумма").pack(pady=5)

        amount_entry = ctk.CTkEntry(edit_window, width=300)
        amount_entry.pack(pady=5)
        amount_entry.insert(0, str(amount))

        # Категория
        ctk.CTkLabel(edit_window, text="Категория").pack(pady=5)

        category_menu = ctk.CTkOptionMenu(
            edit_window,
            values=[
                "Продукты",
                "Транспорт",
                "Развлечения",
                "Здоровье",
                "Одежда",
                "Зарплата",
                "Подработка",
                "Подарки",
                "Другое"
            ],
            width=300
        )
        category_menu.pack(pady=5)
        category_menu.set(category)

        # Описание
        ctk.CTkLabel(edit_window, text="Описание").pack(pady=5)

        description_entry = ctk.CTkEntry(edit_window, width=300)
        description_entry.pack(pady=5)
        description_entry.insert(0, description or "")

        # Дата
        ctk.CTkLabel(edit_window, text="Дата (ГГГГ-ММ-ДД)").pack(pady=5)

        date_entry = ctk.CTkEntry(edit_window, width=300)
        date_entry.pack(pady=5)
        date_entry.insert(0, date)

        # Сохранение изменений
        def save_changes():
            try:
                new_amount = float(amount_entry.get().replace(",", "."))

                if new_amount <= 0:
                    raise ValueError

                new_date = date_entry.get().strip()
                datetime.strptime(new_date, "%Y-%m-%d")

                update_transaction(
                    transaction_id,
                    type_menu.get(),
                    new_amount,
                    category_menu.get(),
                    description_entry.get().strip(),
                    new_date
                )

                messagebox.showinfo(
                    "Успех",
                    "Операция успешно изменена!"
                )

                edit_window.destroy()
                self.show_transactions()

            except ValueError:
                messagebox.showerror(
                    "Ошибка",
                    "Проверь сумму и дату. Сумма должна быть больше нуля."
                )

        save_button = ctk.CTkButton(
            edit_window,
            text="Сохранить изменения",
            command=save_changes,
            width=300,
            height=40,
            fg_color="#8B5CF6",
            hover_color="#7041D8"
        )
        save_button.pack(pady=20)

    def edit_operation(self, transaction_id):
        transaction = get_transaction_by_id(transaction_id)

        if not transaction:
            messagebox.showerror("Ошибка", "Операция не найдена.")
            return

        # Получаем данные операции
        _, transaction_type, amount, category, description, date = transaction

        # Создаём окно редактирования
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Редактирование операции")
        edit_window.geometry("450x550")
        edit_window.resizable(False, False)
        edit_window.grab_set()

        # Заголовок
        ctk.CTkLabel(
            edit_window,
            text="Изменить операцию",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        # Тип операции
        ctk.CTkLabel(edit_window, text="Тип операции").pack(pady=5)

        type_menu = ctk.CTkOptionMenu(
            edit_window,
            values=["Расход", "Доход"],
            width=300
        )
        type_menu.pack(pady=5)
        type_menu.set(transaction_type)

        # Сумма
        ctk.CTkLabel(edit_window, text="Сумма").pack(pady=5)

        amount_entry = ctk.CTkEntry(edit_window, width=300)
        amount_entry.pack(pady=5)
        amount_entry.insert(0, str(amount))

        # Категория
        ctk.CTkLabel(edit_window, text="Категория").pack(pady=5)

        category_menu = ctk.CTkOptionMenu(
            edit_window,
            values=[
                "Продукты",
                "Транспорт",
                "Развлечения",
                "Здоровье",
                "Одежда",
                "Зарплата",
                "Подработка",
                "Подарки",
                "Другое"
            ],
            width=300
        )
        category_menu.pack(pady=5)
        category_menu.set(category)

        # Описание
        ctk.CTkLabel(edit_window, text="Описание").pack(pady=5)

        description_entry = ctk.CTkEntry(edit_window, width=300)
        description_entry.pack(pady=5)
        description_entry.insert(0, description or "")

        # Дата
        ctk.CTkLabel(edit_window, text="Дата (ГГГГ-ММ-ДД)").pack(pady=5)

        date_entry = ctk.CTkEntry(edit_window, width=300)
        date_entry.pack(pady=5)
        date_entry.insert(0, date)

        # Сохранение изменений
        def save_changes():
            try:
                new_amount = float(amount_entry.get().replace(",", "."))

                if new_amount <= 0:
                    raise ValueError

                new_date = date_entry.get().strip()
                datetime.strptime(new_date, "%Y-%m-%d")

                update_transaction(
                    transaction_id,
                    type_menu.get(),
                    new_amount,
                    category_menu.get(),
                    description_entry.get().strip(),
                    new_date
                )

                messagebox.showinfo(
                    "Успех",
                    "Операция успешно изменена!"
                )

                edit_window.destroy()
                self.show_transactions()

            except ValueError:
                messagebox.showerror(
                    "Ошибка",
                    "Проверь сумму и дату. Сумма должна быть больше нуля."
                )

        save_button = ctk.CTkButton(
            edit_window,
            text="Сохранить изменения",
            command=save_changes,
            width=300,
            height=40,
            fg_color="#8B5CF6",
            hover_color="#7041D8"
        )
        save_button.pack(pady=20)
    def show_settings(self):
        title = ctk.CTkLabel(
            self.content,
            text="Настройки приложения",
            font=("Arial", 24, "bold"),
            text_color="white"
        )
        title.grid(row=1, column=0, pady=20)

        budget_label = ctk.CTkLabel(
            self.content,
            text="Месячный бюджет (₽)",
            font=("Arial", 16),
            text_color="white"
        )
        budget_label.grid(row=2, column=0, pady=10)

        self.budget_entry = ctk.CTkEntry(
            self.content,
            placeholder_text="Введите сумму бюджета",
            width=250
        )
        self.budget_entry.grid(row=3, column=0, pady=10)

        current_budget = get_monthly_budget()

        if current_budget > 0:
            self.budget_entry.insert(0, str(current_budget))
        monthly_expenses = get_monthly_expenses()
        remaining = current_budget - monthly_expenses

        save_button = ctk.CTkButton(
            self.content,
            text="Сохранить бюджет",
            command=self.save_budget,
            fg_color="#8B5CF6",
            hover_color="#7C3AED"
        )
        save_button.grid(row=4, column=0, pady=15)

        if current_budget > 0:
            info_label = ctk.CTkLabel(
                self.content,
                text=f"Текущий бюджет: {current_budget:.2f} ₽",
                font=("Arial", 15),
                text_color="#A0A0B0"
            )
            info_label.grid(row=5, column=0, pady=10)
        expenses_label = ctk.CTkLabel(
            self.content,
            text=f"Потрачено за месяц: {monthly_expenses:.2f} ₽",
            font=("Arial", 15),
            text_color="#EF4444"
        )
        expenses_label.grid(row=6, column=0, pady=10)

        remaining_color = "#22C55E" if remaining >= 0 else "#EF4444"

        remaining_label = ctk.CTkLabel(
            self.content,
            text=f"Осталось: {remaining:.2f} ₽",
            font=("Arial", 17, "bold"),
            text_color=remaining_color
        )
        remaining_label.grid(row=7, column=0, pady=10)


    def save_budget(self):
        try:
            amount = float(self.budget_entry.get().replace(",", "."))

            if amount <= 0:
                messagebox.showerror(
                    "Ошибка",
                    "Бюджет должен быть больше нуля."
                )
                return

            set_monthly_budget(amount)

            messagebox.showinfo(
                "Успех",
                "Месячный бюджет сохранён!"
            )

            self.show_page("Настройки")

        except ValueError:
            messagebox.showerror(
                "Ошибка",
                "Введите корректную сумму."
            )

# Запуск приложения
if __name__ == "__main__":

    create_table()

    app = MoneyTrackApp()
    app.mainloop()