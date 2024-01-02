import sqlite3

# conn = sqlite3.connect('LiTracker.db')
# cursor = conn.cursor()

class LiTrackerDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('LiTracker.db')
        self.cursor = self.conn.cursor()

    def init_database(self):
        """Инициирует таблицы в базе данных."""

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            user_id INTEGER
        )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS limits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER, 
                daily_rapid_limit INTEGER DEFAULT 5,
                daily_blitz_limit  DEFAULT 10,
                rapid_games_played_daily INTEGER DEFAULT 0, 
                blitz_games_played_daily INTEGER DEFAULT 0, 
                daily_puzzles_limit INTEGER DEFAULT 20, 
                daily_puzzles_played INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES User(id) 
            )
            ''')

        # Применяем изменения в базе данных
        self.conn.commit()

        # Закрываем соединение с базой данных
        self.conn.close()

        print("База данных и таблица User созданы успешно.")

    def add_player(self, username, user_id):
        # SQL-запрос для вставки нового игрока в таблицу User
        insert_query = '''
                INSERT INTO User (username, user_id) VALUES (?, ?)
            '''
        try:
            # Выполнение запроса
            self.cursor.execute(insert_query, (username, user_id))
            # Фиксация изменений
            self.conn.commit()
            print(f"Игрок с именем {username} успешно добавлен.")
        except sqlite3.IntegrityError:
            print(f"Игрок с именем {username} уже существует.")
        except sqlite3.Error as e:
            print(f"Произошла ошибка при добавлении игрока: {e}")

        # Добавляем лимиты

        insert_query = '''
                        INSERT INTO Limits (user_id) VALUES (?)
                    '''
        try:
            # Выполнение запроса
            self.cursor.execute(insert_query, (user_id, ))
            # Фиксация изменений
            self.conn.commit()
            print(f"Лимит партий для юзера {user_id} успешно добавлен.")
        except sqlite3.IntegrityError:
            print(f"Лимит партий для юзера {user_id} уже существует.")
        except sqlite3.Error as e:
            print(f"Произошла ошибка при добавлении лимита: {e}")



