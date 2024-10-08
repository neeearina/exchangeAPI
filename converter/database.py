import sqlite3

import settings


# подключение к базе данных
def connect_db():
    return sqlite3.connect(settings.DATABASE)


# создание таблицы
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exchange_rates (
            currency TEXT PRIMARY KEY,
            rate REAL NOT NULL,
            last_updated DATETIME NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
