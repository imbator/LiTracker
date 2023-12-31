# import requests
#
#
# # Инициирование анализа
# response = requests.post(f'https://lichess.org/api/game/{ID_ПАРТИИ}/analysis', headers=headers)
#
# # Проверка, что анализ начат
# if response.status_code == 200:
#     print("Анализ запущен")
#
# # Получение анализированной PGN партии
# pgn_response = requests.get(f'https://lichess.org/game/export/{ID_ПАРТИИ}', headers=headers)
#
# if pgn_response.status_code == 200:
#     pgn_text = pgn_response.text
#     # Теперь pgn_text содержит PGN данных с пометками анализа
#     print(pgn_text)