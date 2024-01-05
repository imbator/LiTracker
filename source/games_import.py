from berserk import Client
from telegram.ext import  CallbackContext
from config import player
from database import LiTrackerDatabase

class GamesTracker:
    def __init__(self, client):
        self.client = client
        self.download_last_game(player)
        self.db = LiTrackerDatabase()

    def get_last_game_id(self, player_name):
        """Возвращает айди последней игры для данного пользователя."""
        last_game = list(self.client.games.export_by_player(player_name, max=1))[0]
        return last_game['id']
    def download_last_game(self, player_name):
        """Loading last game from lichess servers."""
        last_game_id = self.get_last_game_id(player_name)
        data = self.client.games.export(last_game_id)
        print(data['id'])
        print(data['players']['white']['user']['name'])
        print(data['players']['black'])
        print(data['opening']['name'])

    async def check_new_game(self, context: CallbackContext):
        """Проверяет наличие новой игры на сервере lichess."""

        job = context.job
        chat_id = job.chat_id
        user_id = job.user_id

        last_game = list(self.client.games.export_by_player(player, max=1))[0]

        player_name = job.data['player_name']
        last_game_id_prev = job.data['last_game_id']
        last_game_id_new = last_game['id']

        if last_game_id_prev != last_game_id_new:
            # Зафиксирована новая игра
            await context.bot.send_message(chat_id=chat_id, text=f"У пользователя {player_name} появилась новая игра!")

            # Экспортируем игру с анализом
            data = self.client.games.export(last_game_id_new)
            self.db.add_game_to_database(user_id, player_name, data)

        job.data['last_game_id'] = last_game_id_new

        print(last_game_id_new, last_game_id_prev)


    async def start_checking_for_new_game(self, update, context):
        chat_id = update.message.chat_id
        user_id = update.effective_user.id

        player_name = player # При многопользовательской работе должен получать информацию из базы данных по айди юзера
        last_game_id = self.get_last_game_id(player_name)

        # Создаем и запускаем задачу для проверки новой игры
        context.job_queue.run_repeating(
            self.check_new_game,
            interval=5,  # Интервал проверки в секундах
            first=0,  # Начать выполнение немедленно
            data={'player_name': player_name, 'last_game_id': last_game_id},
            chat_id=chat_id,
            user_id=user_id
        )
        await update.message.reply_text(f"Начинаем отслеживать игры пользователя {player_name}.")

    @staticmethod
    def stop_checking(update, context):
        # Останавливаем все задачи в JobQueue
        context.job_queue.stop()
        update.message.reply_text("Отслеживание игр остановлено.")


    def load_game_to_database(self):
        """Инициирование загрузки новой игры в базу данных"""


    #TODO
    def load_chess_base(self) -> None:
        """Download a new chessbase into the system."""
        pass


