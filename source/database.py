import sqlite3

# conn = sqlite3.connect('LiTracker.db')
# cursor = conn.cursor()

def init_database():
    """Инициирует подключение к базе данных."""
    conn = sqlite3.connect('LiTracker.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE
    )
    ''')

    # Применяем изменения в базе данных
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()

    print("База данных и таблица User созданы успешно.")

