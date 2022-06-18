import os
import pickle
from flask import Flask, request
from flask_app.games import Games
from engine_module.board import Board
from engine_module.engine import Engine

app = Flask(__name__)
game = Engine(Board(9), "black", 0)
list_of_games = Games()


@app.route('/createGame', methods=['POST'])
def create_game():
    game_id = request.args.get("game_id")
    is_handicap = request.args.get("is_handicap")
    if is_handicap == "yes":
        handicap_board = Board(9)
        handicap_board.array[2][2] = 1
        handicap_board.array[6][2] = 1
        handicap_board.array[2][6] = 1
        handicap_board.array[6][6] = 1
        list_of_games.add_game(game_id, Engine(handicap_board, "white", 0))
        list_of_games.games_list[game_id].board.print_board()
        return f'Game created:\n {list_of_games.games_list[game_id].board.array_to_string} '
    elif is_handicap == "no":
        list_of_games.add_game(game_id, Engine(Board(9), "black", 0))
        list_of_games.games_list[game_id].board.print_board()
        return f'Game created:\n {list_of_games.games_list[game_id].board.array_to_string} '
    else:
        return "Wrong answer!"


@app.route('/game/player1', methods=['GET'])
def player1():
    move = request.args.get("move")
    game_id = request.args.get("game_id")
    list_of_games.games_list[game_id].place_stone(int(move.split(",")[0]), int(move.split(",")[1]))
    list_of_games.games_list[game_id].board.print_board()
    return f'Game id: {game_id}, Current turn: {list_of_games.games_list[game_id].turn_color}\n' \
           f'Board:\n {list_of_games.games_list[game_id].board.array_to_string}'


@app.route('/game/player2', methods=['GET'])
def player2():
    move = request.args.get("move")
    game_id = request.args.get("game_id")

    list_of_games.games_list[game_id].place_stone(int(move.split(",")[0]), int(move.split(",")[1]))
    list_of_games.games_list[game_id].board.print_board()
    return f'Game id: {game_id}, Current turn: {list_of_games.games_list[game_id].turn_color}\n' \
           f'Board:\n {list_of_games.games_list[game_id].board.array_to_string}'


@app.route('/endGame', methods=['GET'])
def end_game():
    game_id = request.args.get("game_id")
    list_of_games.games_list[game_id].show_result()
    return f'Game ended \n{list_of_games.games_list[game_id].result}'


@app.route('/deleteGame', methods=['POST'])
def delete_game():
    game_id = request.args.get("game_id")
    list_of_games.delete_game(game_id)
    return f'Game deleted, id: {game_id} \n Games={list_of_games.games_list}'


@app.route('/saveGame', methods=['POST'])
def save_game_to_file():
    game_id = request.args.get("game_id")
    file_name = request.args.get("file_name")
    game_state = list_of_games.games_list[game_id]
    with open(file_name + ".pickle", "wb") as file:
        pickle.dump(game_state, file)

    return f'Game saved in file: {file_name}'


@app.route('/loadGame', methods=['GET'])
def load_game_from_file():
    game_id = request.args.get("game_id")
    file_name = request.args.get("file_name")
    with open(file_name + ".pickle", 'rb') as file:
        list_of_games.games_list[game_id] = pickle.load(file)
    list_of_games.games_list[game_id].board.print_board()

    return f'Game loaded: \n' \
           f'{list_of_games.games_list[game_id].board.array_to_string}'


@app.route('/createGameFile', methods=['POST'])
def create_game_file():
    game_id = request.args.get("game_id")
    is_handicap = request.args.get("is_handicap")
    if is_handicap == "yes":
        handicap_board = Board(9)
        handicap_board.array[2][2] = 1
        handicap_board.array[6][2] = 1
        handicap_board.array[2][6] = 1
        handicap_board.array[6][6] = 1
        new_game = Engine(handicap_board, "white", 0)
        list_of_games.handle_as_file(game_id, new_game)
        list_of_games.load_from_file(game_id).board.print_board()
        return f'Game created:\n {list_of_games.load_from_file(game_id).board.array_to_string} '
    elif is_handicap == "no":
        new_game = Engine(Board(9), "black", 0)
        list_of_games.handle_as_file(game_id, new_game)
        list_of_games.load_from_file(game_id).board.print_board()
        return f'Game created:\n {list_of_games.load_from_file(game_id).board.array_to_string} '
    else:
        return "Wrong answer!"


@app.route('/player1file', methods=['GET'])
def player1_file():
    move = request.args.get("move")
    game_id = request.args.get("game_id")
    current_game = list_of_games.load_from_file(game_id)
    current_game.place_stone(int(move.split(",")[0]), int(move.split(",")[1]))
    current_game.board.print_board()
    list_of_games.handle_as_file(game_id, current_game)

    return f'Game id: {game_id}, Current turn: {current_game.turn_color}\n' \
           f'Board:\n {current_game.board.array_to_string}'


@app.route('/player2file', methods=['GET'])
def player2_file():
    move = request.args.get("move")
    game_id = request.args.get("game_id")
    current_game = list_of_games.load_from_file(game_id)
    current_game.place_stone(int(move.split(",")[0]), int(move.split(",")[1]))
    current_game.board.print_board()
    list_of_games.handle_as_file(game_id, current_game)

    return f'Game id: {game_id}, Current turn: {current_game.turn_color}\n' \
           f'Board:\n {current_game.board.array_to_string}'


@app.route('/endGameFile', methods=['GET'])
def end_game_file():
    game_id = request.args.get("game_id")
    list_of_games.load_from_file(game_id).show_result()
    return f'Game ended \n{list_of_games.load_from_file(game_id).result}'


@app.route('/deleteGameFile', methods=['POST'])
def delete_game_file():
    game_id = request.args.get("game_id")
    os.remove("Game_" + str(game_id) + ".pickle")

    return f'Game deleted, id: {game_id}'


if __name__ == '__main__':
    app.run(debug=True)
