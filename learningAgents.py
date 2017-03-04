

from agents import Agent
import math
import random
import numpy as np
import tensorflow as tf



class LearningAgent(Agent):
    def __init__(self, tile, game):
        super(LearningAgent, self).__init__(tile, game)

    def getMove(self):
        possibleMoves = self.game.getValidMoves(self.game.board, self.tile)
        random.shuffle(possibleMoves)
        for x, y in possibleMoves:
            if self.game.isOnCorner(x, y):
                return [x, y]
        bestScore = -1
        bestMove = [-1, -1]
        for x, y in possibleMoves:
            dupeBoard = self.game.getBoardCopy(self.game.board)
            self.game.makeMove(dupeBoard, self.tile, x, y)
            score = self.game.getScoreOfBoard(dupeBoard)[self.tile]
            if score > bestScore:
                bestMove = [x, y]
                bestScore = score
        return bestMove


