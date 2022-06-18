import itertools

import numpy
import networkx


class Engine:

    def __init__(self, board, turn_color, count_passes):
        self.board = board
        self.turn_color = turn_color
        self.count_passes = count_passes
        self.prisoners = [0, 0]
        self.result = ""

    def has_liberties(self, group):
        for x, y in group:
            if x > 0 and self.board.array[x - 1, y] == 0:
                return True
            if y > 0 and self.board.array[x, y - 1] == 0:
                return True
            if x < self.board.size - 1 and self.board.array[x + 1, y] == 0:
                return True
            if y < self.board.size - 1 and self.board.array[x, y + 1] == 0:
                return True
        return False

    def get_groups(self, color):
        size = self.board.size
        if color == "black":
            color_code = 1
        else:
            color_code = 2
        xs, ys = numpy.where(self.board.array == color_code)
        graph = networkx.grid_graph(dim=[size, size])
        stones = set(zip(xs, ys))
        all_spaces = set(itertools.product(range(size), range(size)))
        stones_to_remove = all_spaces - stones
        graph.remove_nodes_from(stones_to_remove)
        return networkx.connected_components(graph)

    def is_valid(self, x, y):
        if x < 0 or x >= self.board.size:
            return False
        if y < 0 or y >= self.board.size:
            return False
        return self.board.array[x, y] == 0

    def place_stone(self, x, y):
        if not self.is_valid(x, y):
            print("Invalid move!")
            return

        if self.turn_color == "black":
            self.board.array[x, y] = 1
            opponent_color = "white"
        else:
            self.board.array[x, y] = 2
            opponent_color = "black"

        capture_happened = False
        for group in list(self.get_groups(opponent_color)):
            if not self.has_liberties(group):
                capture_happened = True
                for x, y in group:
                    self.board.array[x, y] = 0
                    self.board.array_to_print[x][y] = "."
                if self.turn_color == "black":
                    self.prisoners[0] += len(group)
                else:
                    self.prisoners[1] += len(group)

        if not capture_happened:
            group = None
            for group in self.get_groups(self.turn_color):
                if (x, y) in group:
                    break
            if not self.has_liberties(group):
                self.board.array[x, y] = 0
                print("Invalid move!")
                return

        self.turn_color = opponent_color
        self.count_passes = 0

    def pass_move(self):
        self.count_passes += 1
        if self.turn_color == "black":
            self.turn_color = "white"
        else:
            self.turn_color = "black"

    def show_result(self):
        black_points = self.prisoners[0]
        white_points = self.prisoners[1]
        self.result = ""
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.board.array_to_print[x][y] == "B":
                    black_points += 1
                elif self.board.array_to_print[x][y] == "W":
                    white_points += 1

        if self.board.array_to_print[4][4] == "B":
            black_points += 1
        elif self.board.array_to_print[4][4] == "W":
            white_points += 1

        print("Black player score is " + str(black_points))
        self.result += "Black player score is " + str(black_points) + "\n"
        print("White player score is " + str(white_points))
        self.result += "White player score is " + str(white_points) + "\n"
        if black_points > white_points:
            print("Black player won!")
            self.result += "Black player won!"
        elif black_points < white_points:
            print("White player won!")
            self.result += "White player won!"
        else:
            print("Draw!")
            self.result += "Draw!"
