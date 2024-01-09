import berserk
from config import API_TOKEN


from bot import Bot
from games_import import GamesTracker

session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session)

if __name__ == '__main__':
    bot = Bot(client)
    bot.games_analyser.find_opening_in_pgn("bases/ruy_lopez.pgn", 2)
    importer = GamesTracker(client)
    # data_ruy_lopez = importer.parse_pgn_base("bases/ruy_lopez.pgn")
    # data_e4_white = importer.parse_pgn_base("bases/jan_gustafssons_e4.pgn")
    data_e4_black = importer.parse_pgn_base("bases/anish_giri_e4.pgn")
    # data_d4_black = importer.parse_pgn_base("bases/qgd.pgn")

    for game in data_e4_black:
        print(game)



    # bot.start()


