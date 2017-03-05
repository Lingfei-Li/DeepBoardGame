

from learningAgents import LearningAgent
from othello import Othello
from agents import MinimaxAgent, GreedyAgent, AlphaBetaAgent
import matplotlib.pyplot as plt

class Environment:
    def __init__(self, game):
        self.game = game
        self.done = False
        self.skip = False

    def getState(self, board, tile):
        myMap = [0] * 64
        rivalMap = [0] * 64
        validMoves = [0] * 64
        for x in range(8):
            for y in range(8):
                pos = x * 8 + y
                if board[x][y] == tile:
                    myMap[pos] = 1
                elif board[x][y] == 'O' or board[x][y] == 'X':
                    rivalMap[pos] = 1
        possibleMoves = self.game.getValidMoves(board, tile)
        for x, y in possibleMoves:
            pos = x * 8 + y
            validMoves[pos] = 1

        return myMap + rivalMap + validMoves

    def step(self, action, tile):
        self.skip = False
        game = self.game
        tile2 = 'X' if tile=='O' else 'O'

        game.makeMove(game.board, tile, action[0], action[1])
        if game.getValidMoves(game.board, tile2) == []:
            if game.getValidMoves(game.board, tile1) == []:
                self.done = True
            else:
                self.skip = True

        return self.getState(game.board, tile)

    def reset(self):
        self.game.resetBoard()
        self.done = False


game = Othello()
tile1 = 'O'
tile2 = 'X'
env = Environment(game)
agent1 = LearningAgent(tile1, game, env)
agent2 = AlphaBetaAgent(tile2, game, 4)
maxEpoch = 200
epoch = 0
performance = []
while epoch < maxEpoch:
    epoch += 1
    env.reset()
    while not env.done:
        if env.skip == False:
            x1, y1 = agent1.train_step()
            if not env.done:
                env.step([x1, y1], tile1)
            else:
                break
        else:
            env.skip = False

        if env.skip == False:
            x2, y2 = agent2.getMove()
            if not env.done:
                env.step([x2, y2], tile2)
            if env.done:
                agent1.train_step()
        else:
            env.skip = False

    game.drawBoard(game.board)
    scores = game.getScoreOfBoard(game.board)
    print('Epoch #', epoch)
    print('Score:', scores[tile1]-scores[tile2])
    performance.append(scores[tile1] - scores[tile2])
    corners = game.cornersHeld(game.board)
    print('Corners held:', corners[tile1])

print('Win rate:', [x for x in performance if x>0])
print('Lose rate:', [x for x in performance if x<0])
print('Corners held:', corners)
plt.plot(performance, 'o')
plt.show()




