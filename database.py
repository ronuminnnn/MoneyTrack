import sqlite3
import os

APP_DIR = os.path.expanduser("~/Library/Application Support/MoneyTrack")
os.makedirs(APP_DIR, exist_ok=True)
DB_PATH = os.path.join(APP_DIR, "finance.db")
from datetime import datetime
# Подключение к базе данных
def connect_db():
    connection = sqlite3.connect(DB_PATH)
    return connection


# Создание таблицы операций
def create_table():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# Добавление операции
def add_transaction(
    transaction_type,
    amount,
    category,
    description,
    date
):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (type, amount, category, description, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        transaction_type,
        amount,
        category,
        description,
        date
    ))

    connection.commit()
    connection.close()


# Получение всех операций
def get_transactions():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM transactions ORDER BY date DESC, id DESC"
    )

    transactions = cursor.fetchall()

    connection.close()

    return transactions

def get_transaction_by_id(transaction_id):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    transaction = cursor.fetchone()

    connection.close()

    return transaction

# Удаление операции
def delete_transaction(transaction_id):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    connection.commit()
    connection.close()


# Редактирование операции
def update_transaction(
    transaction_id,
    transaction_type,
    amount,
    category,
    description,
    date
):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE transactions
        SET type = ?,
            amount = ?,
            category = ?,
            description = ?,
            date = ?
        WHERE id = ?
    """, (
        transaction_type,
        amount,
        category,
        description,
        date,
        transaction_id
    ))

    connection.commit()
    connection.close()


# Расчёт баланса
def get_balance():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            SUM(CASE WHEN type = 'Доход' THEN amount ELSE 0 END),
            SUM(CASE WHEN type = 'Расход' THEN amount ELSE 0 END)
        FROM transactions
    """)

    income, expenses = cursor.fetchone()

    connection.close()

    income = income or 0
    expenses = expenses or 0

    return income - expenses
# Получение общей суммы доходов и расходов
def get_financial_summary():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            SUM(CASE WHEN type = 'Доход' THEN amount ELSE 0 END),
            SUM(CASE WHEN type = 'Расход' THEN amount ELSE 0 END)
        FROM transactions
    """)

    income, expenses = cursor.fetchone()

    connection.close()

    return income or 0, expenses or 0

# Получение расходов по категориям
def get_expenses_by_category():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE type = 'Расход'
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses

def set_monthly_budget(amount):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            monthly_budget REAL NOT NULL
        )
    """)

    cursor.execute("""
        INSERT OR REPLACE INTO settings (id, monthly_budget)
        VALUES (1, ?)
    """, (amount,))

    connection.commit()
    connection.close()


def get_monthly_budget():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            monthly_budget REAL NOT NULL
        )
    """)

    cursor.execute("SELECT monthly_budget FROM settings WHERE id = 1")
    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return 0

def get_monthly_expenses():
    connection = connect_db()
    cursor = connection.cursor()

    current_month = datetime.now().strftime("%Y-%m")

    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type = 'Расход'
        AND date LIKE ?
    """, (current_month + "%",))

    result = cursor.fetchone()
    connection.close()

    return result[0] or 0

# Создание таблицы при запуске
if __name__ == "__main__":
    create_table()
    print("База данных успешно создана!")
