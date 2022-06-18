import numpy


class Board:

    def __init__(self, size):
        self.size = size
        self.array = numpy.zeros((size, size))
        self.array_to_print = [["." for x in range(size)] for y in range(size)]

    def print_board(self):
        for x in range(self.size):
            for y in range(self.size):
                if int(self.array[x, y]) == 0:
                    continue
                elif self.array[x, y] == 1:
                    self.array_to_print[x][y] = "B"
                elif self.array[x, y] == 2:
                    self.array_to_print[x][y] = "W"
        print("   0 1 2 3 4 5 6 7 8")
        print("--------------------")
        for x in range(self.size):
            for y in range(self.size):
                if y == 0:
                    print(str(x) + "|", end=" ")
                print(self.array_to_print[x][y], end=" ")
            print()
