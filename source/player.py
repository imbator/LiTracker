from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackContext
)

async def register_player(player_name: str):
    """Регистрирует текущего игрока в системе."""
    pass

# Определяем состояния разговора
REGISTER, END_REGISTER = range(2)

async def start_register(update: Update, context: CallbackContext) -> int:
    # Пользователю отправляется приглашение к вводу
    await update.message.reply_text('Please, enter your lichess account nickname: ')
    # Переходим в состояние INPUT_TEXT
    return REGISTER

async def input_text(update: Update, context: CallbackContext) -> int:
    # Чтение текста, введенного пользователем
    # user_text = update.message.text
    await update.message.reply_text(f'smth')
    return END_REGISTER

async def end_registration(update: Update, context: CallbackContext):
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    # Пользователь отменил ввод
    await update.message.reply_text('Операция отменена.')
    # Завершаем разговор
    return ConversationHandler.END

# Определение точки входа в разговор
start_handler = CommandHandler('register', start_register)

# Определение обработчика для каждого состояния разговора
conversation_handler = ConversationHandler(
    entry_points=[start_handler],
    states={
        REGISTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, input_text)],
        END_REGISTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, end_registration)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

