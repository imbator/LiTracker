import berserk
from config import API_TOKEN, player, BOT_TOKEN
from games_import import download_last_game
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import Update
from database import init_database

session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session)
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello, {update.effective_user.first_name}!')

if __name__ == '__main__':
    download_last_game(player, client)
    init_database()

    app = ApplicationBuilder().token(BOT_TOKEN ).build()
    app.add_handler(MessageHandler(filters.TEXT, hello))
    app.run_polling()

