from berserk import Client
from telegram.ext import  CallbackContext
from config import player

class GamesTracker:
    def __init__(self, client):
        self.client = client

    def get_last_game_id(self, player_name):
        """Возвращает айди последней игры для данного пользователя."""
        last_game = list(self.client.games.export_by_player(player_name, max=1))[0]
        return last_game['id']
    def download_last_game(self, player_name):
        """Loading last game from lichess servers."""
        last_game_id = self.get_last_game_id(player_name)
        # data = client.games.export(game_id, as_pgn=True)
        data = self.client.games.export(last_game_id, as_pgn=True)
        print(data)

    async def check_new_game(self, context: CallbackContext):
        """Проверяет наличие новой игры на сервере lichess."""

        last_game = list(self.client.games.export_by_player(player, max=1))[0]
        last_game_id_new = last_game['id']

        job = context.job
        player_name = job.data['player_name']
        chat_id = job.data['chat_id']

        last_game_id_prev = job.data['last_game_id']

        if last_game_id_prev != last_game_id_new:
            # Зафиксирована новая игра
            await context.bot.send_message(chat_id=chat_id, text=f"У пользователя {player_name} появилась новая игра!")

        job.data['last_game_id'] = last_game_id_new

        print(last_game_id_new)


    async def start_checking_for_new_game(self, update, context):
        chat_id = update.message.chat_id
        player_name = player
        last_game_id = self.get_last_game_id(player_name)

    # Создаем и запускаем задачу для проверки новой игры
        context.job_queue.run_repeating(
            self.check_new_game,
            interval=5,  # Интервал проверки в секундах
            first=0,  # Начать выполнение немедленно
            data={'player_name': player_name, 'chat_id': chat_id, 'last_game_id': last_game_id}
        )
        await update.message.reply_text(f"Начинаем отслеживать игры пользователя {player_name}.")

    @staticmethod
    def stop_checking(update, context):
        # Останавливаем все задачи в JobQueue
        context.job_queue.stop()
        update.message.reply_text("Отслеживание игр остановлено.")

    #TODO
    def load_chess_base(self) -> None:
        """Download a new chessbase into the system."""
        pass
