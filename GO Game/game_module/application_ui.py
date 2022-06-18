import numpy

from engine_module.board import Board
from engine_module.engine import Engine


class ApplicationUI:

    def print_menu(self):
        print("----GO Game----")
        print("1. Start new game")
        print("2. Load game")
        print("0. Quit")

    def main_menu(self):
        board = Board(9)
        game = Engine(board, "black", 0)
        while True:
            self.print_menu()
            print("Choice: ", end=" ")
            choice = int(input())
            if choice == 1:
                game = Engine(Board(9), "black", 0)
                self.create_new_game(game)
                self.play_game(game)
            elif choice == 2:
                print("Enter path to the array file: ", end=" ")
                arr_path = input()
                print("Enter path to the data file: ", end=" ")
                data_path = input()
                self.load_board_from_file(arr_path, data_path, game)
                self.play_game(game)
            elif choice == 0:
                break
            else:
                print("Invalid choice!")

    def save_board_to_file(self, arr_file_path, data_file_path, game):
        file = open(data_file_path, "w")
        file.write(game.turn_color + "\n")
        file.write(str(game.count_passes))
        numpy.savetxt(arr_file_path, game.board.array)
        file.close()

    def load_board_from_file(self, arr_file_path, data_file_path, game):
        file = open(data_file_path, "r")
        line_counter = 0
        for line in file:
            if line_counter == 0:
                game.turn_color = line
            else:
                game.count_passes = line
            line_counter += 1
        game.board.array = numpy.loadtxt(arr_file_path)
        file.close()

    def create_new_game(self, game):
        print("Do you want play with black handicap stones? [y/n]", end=" ")
        answer = input()

        while answer != "y" and answer != "n":
            print("Invalid answer!")
            answer = input()

        if answer == "y":
            game.board.array[2][2] = 1
            game.board.array[6][2] = 1
            game.board.array[2][6] = 1
            game.board.array[6][6] = 1
            game.turn_color = "white"
            game.count_passes = 0
        else:
            game.turn_color = "black"
            game.count_passes = 0

    def play_game(self, game):
        while True:
            game.board.print_board()
            # m - move (dodatkowo musimy podać koordynaty)
            # p - pass
            # s - save (dodatkowo musimy podać ścieżkę do plików tekstowych - 1 z tablicą, 2 z danymi)
            # q - quit
            print(str(game.turn_color) + " turn [m/p/s/q]: ", end=" ")
            command = input().split()

            if command[0] == "m":
                x, y = [int(command[1]), int(command[2])]
                game.place_stone(x, y)
            elif command[0] == "p":
                game.pass_move()
                if game.count_passes == 2:
                    print("Both players passed!")
                    game.show_result()
                    break
            elif command[0] == "s":
                self.save_board_to_file(command[1], command[2], game)
            elif command[0] == "q":
                break
            else:
                print("Invalid command!")
