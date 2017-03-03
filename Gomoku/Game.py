

from Gomoku.board import Board

black = +1
white = -1
player = {-1: "white", 1: "black"}

class Game:
    def __init__(self):
        self.board = Board(50, 50)
        self.player = white

    def take_move(self, x, y):
        print("({},{})".format(x, y))
        self.board[x, y] = self.player
        self.player = -self.player
        return self.check_terminate()

    def check_terminate(self):
        winner, positions = self.board.winner()
        if (winner is not None) or (self.board.full()):
            print("Winner:", player[winner])
            return winner
        return None

game = Game()
while True:
    x = input()
    y = input()
    if game.take_move(x, y) is not None:
        break


