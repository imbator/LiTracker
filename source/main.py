import berserk
from config import API_TOKEN

from bot import Bot

session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session)

if __name__ == '__main__':
    bot = Bot(client)

    bot.start()


