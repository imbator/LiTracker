from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackContext
)

from database import LiTrackerDatabase

databaseUnit = LiTrackerDatabase()


# Определяем состояния разговора
REGISTER = 0

async def start_register(update: Update, context: CallbackContext) -> int:
    # Пользователю отправляется приглашение к вводу
    await update.message.reply_text('Please, enter your lichess account nickname: ')
    return REGISTER

async def end_registration(update: Update, context: CallbackContext) -> int:
    username = update.message.text
    user_id = update.effective_user.id

    # Запоминаем никнейм в базе данных пользователей:
    databaseUnit.add_player(username, user_id)


    await update.message.reply_text(f'Вы успешно зарегистрированы!')
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    # Пользователь отменил ввод
    await update.message.reply_text('Регистрация отменена.')
    # Завершаем разговор
    return ConversationHandler.END

# Определение точки входа в разговор
registration_start_handler = CommandHandler('register', start_register)

# Определение обработчика для каждого состояния разговора
registration_handler = ConversationHandler(
    entry_points=[registration_start_handler],
    states={
        REGISTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, end_registration)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

