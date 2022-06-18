import pickle

from engine_module.engine import Engine


class Games:
    def __init__(self):
        self.games_list = {}

    def add_game(self, game_id,  new_game: Engine):
        self.games_list.update({game_id: new_game})

    def delete_game(self, game_id: int):
        self.games_list = {id: new_game for current_id, new_game in self.games_list.items() if id != game_id}

    def handle_as_file(self, game_id, game):
        with open("Game_" + str(game_id) + ".pickle", "wb") as file:
            pickle.dump(game, file)

    def load_from_file(self, game_id):
        with open("Game_" + str(game_id) + ".pickle", 'rb') as file:
            current_game = pickle.load(file)
        return current_game