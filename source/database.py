import sqlite3
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

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER, 
                nickname TEXT NOT NULL,
                game_id INTEGER,
                opening TEXT NOT NULL,
                win BOOL
            )
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pgn_chapters (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               pgn_name TEXT NOT NULL,
               chapter_name TEXT NOT NULL,
               chapter_number INTEGER,
               moves_sequence TEXT NOT NULL  
            )
        ''')

        # Применяем изменения в базе данных
        self.conn.commit()

        # Закрываем соединение с базой данных
        self.conn.close()

        print("База данных и таблицы созданы успешно.")

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


    def add_game_to_database(self, user_id, nickname, game_data):
        """Добавляет сыгранную игру прользователя в базу данных партий."""

        insert_query = '''
                        INSERT INTO games (user_id, nickname, game_id, opening, win) VALUES (?, ?, ?, ?, ?)
                        '''

        print(game_data)
        game_id = game_data['id']
        game_opening = game_data['opening']['name']
        active_player_color = 'white' if game_data['players']['white']['user']['name'] == nickname else 'black'


        if game_data['players'][active_player_color]['ratingDiff'] > 0:
            win = True
        else:
            win = False

        try:
            self.cursor.execute(insert_query, (user_id, nickname, game_id, game_opening, win))
            self.conn.commit()
            print(f"Партия игрока {nickname} успешно добавлена.")
        except sqlite3.IntegrityError:
            print(f"Партия уже существует.")
        except sqlite3.Error as e:
            print(f"Произошла ошибка при добавлении партии в базу данных: {e}")

    def add_chapter_to_database(self, pgn_name, chapter_name, chapter_number, moves_sequence):
        """Добавление новой главы из базы данных."""

        insert_query =  '''
                        INSERT INTO pgn_chapters (pgn_name, chapter_name, chapter_number, moves_sequence) 
                        VALUES (?, ?, ?, ?, ?)
                        '''
        try:
            self.cursor.execute(insert_query, (pgn_name, chapter_name, chapter_number, moves_sequence))
            self.conn.commit()
            print(f"Глава {chapter_name} из репертуара {pgn_name} успешно добавлена.")
        except sqlite3.IntegrityError:
            print(f"Глава уже существует.")
        except sqlite3.Error as e:
            print(f"Произошла ошибка при добавлении главы в базу данных: {e}")

    @staticmethod
    def parse_pgn_base(pgn_path):
        """Добавление новой базы pgn партий в базу данных."""
        with open(pgn_path) as pgn_file:
            games_data = []
            game_number = 1
            while True:
                game = chess.pgn.read_game(pgn_file)
                if game is None:
                    break  # Закончились игры в файле
                game_info = {
                    'chapter_name': game.headers.get('Event', 'Unknown Event'),
                    'chapter_number': game_number,
                    'moves': game.board().variation_san(game.mainline_moves())
                }
                games_data.append(game_info)
                game_number += 1
            return games_data

