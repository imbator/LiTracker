from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

from telegram import Update
from config import BOT_TOKEN
from player import registration_handler
from games_import import GamesTracker
from database import LiTrackerDatabase
from games_analisys import GameAnalyser

class Bot:
    def __init__(self, client):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.client = client
        self.games_tracker = GamesTracker(client)
        self.setup_handlers()
        self.database_unit = LiTrackerDatabase()
        self.games_analyser = GameAnalyser()
    @staticmethod
    async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Сообщение выводится при инициализации диалога с новым пользователем или с незалогиненным."""
        await update.message.reply_text(f'Hello, {update.effective_user.first_name}! '
                                        f'I am smart bot, who make your game style analysys. '
                                        f'Do /register to register your account.')
    def setup_handlers(self):
        """Производит установку хендлеров для данного бота."""
        print("added")
        self.application.add_handler(registration_handler)
        self.application.add_handler(CommandHandler("start_tracking", self.games_tracker.start_checking_for_new_game))
        self.application.add_handler(MessageHandler(filters.TEXT, self.hello))

    def start(self):
        """Запускает поллинг бота."""
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

