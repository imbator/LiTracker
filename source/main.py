import berserk
from config import API_TOKEN, player, BOT_TOKEN
from games_import import download_last_game
from telegram.ext import ApplicationBuilder, Updater, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import Update
from player import conversation_handler

session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session)
# dispatcher = updater.D


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello, {update.effective_user.first_name}! '
                                    f'I am smart bot, who make your game style analysys. '
                                    f'Do /register to register your account.')

async def init_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Пожалуйста, введите свой никнейм lichess-аккаунта:')

if __name__ == '__main__':
    download_last_game(player, client)

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(conversation_handler)
    app.add_handler(MessageHandler(filters.TEXT, hello))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


