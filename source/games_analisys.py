import chess.pgn

class GameAnalyser:
    """Класс занимается сопоставлением партии с репертуарником в формате pgn."""
    def __init__(self):
        print("Анализатор партий успешно создан.")

    def show_last_game_moves(self):
        """Выводит на экран ходы из главы chapter файла pgn_path."""
        pass

    @staticmethod
    def find_opening_in_pgn(pgn_path, chapter):
        """Поиск дебюта в базе pgn."""
        with open(pgn_path, 'r') as pgn_file:
            game_counter = 1
            moves_data = ''
            while True:

                game = chess.pgn.read_game(pgn_file)
                if game is None:
                    break  # Закончились игры в файле
                if game_counter == chapter:
                    print(f"Moves from chapter {chapter}:")
                    # Вывести все ходы партии
                    node = game
                    while node.variations:
                        next_node = node.variation(0)
                        moves_data += node.board().san(next_node.move) + ' '
                        print(node.board().san(next_node.move), end=' ')
                        moves_data += node.board().san(next_node.move) + ' '
                        node = next_node
                    print("\n")
                    break  # Вывели нужную главу, выходим из цикла
                game_counter += 1
            print(f"Полученные данные об игре в pgn: {moves_data}")

    @staticmethod
    def check_game_similarity(base_moves_str, recent_game_moves_str, similarity_threshold=5):
        base_moves = base_moves_str.split()
        recent_game_moves = recent_game_moves_str.split()

        # Подсчет количества совпадающих ходов с начала списка
        similar_moves_count = 0
        for base_move, recent_game_move in zip(base_moves, recent_game_moves):
            if base_move == recent_game_move:
                similar_moves_count += 1
            else:
                break  # Прерываем цикл при первом несовпадении

        # Проверяем, достигнут ли порог похожести
        return similar_moves_count >= similarity_threshold


