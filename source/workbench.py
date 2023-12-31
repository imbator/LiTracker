import requests
from config import API_TOKEN

def try_analisys():
    # Ваш токен доступа к API
    api_token = API_TOKEN

    # ID партии
    game_id = 'AsI5VNZy'

    # URL для запроса анализа партии
    url = f'https://lichess.org/api/game/{game_id}/analysis'

    # Заголовки запроса
    headers = {
        'Authorization': f'Bearer {api_token}'
    }

    # Отправка запроса
    response = requests.get(url, headers=headers)

    # Проверка успешности запроса и обработка ответа
    if response.status_code == 200:
        analysis_data = response.json()
        # Обработка данных анализа
        print(analysis_data)
    else:
        print("Ошибка при запросе анализа партии")