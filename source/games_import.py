from berserk import Client
def download_last_game(player_name: str, client: Client):
    """Loading last game from lichess servers."""
    last_game = list(client.games.export_by_player(player_name, max=1))[0]
    game_id = last_game['id']
    # data = client.games.export(game_id, as_pgn=True)
    data = client.games.export(game_id, as_pgn=True)
    print(f"Game id: {game_id}")
    print(data)

def load_chess_base() -> None:
    """Download a new chessbase into the system."""
    pass
