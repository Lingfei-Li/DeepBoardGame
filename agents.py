
import random

MAX_VALUE = 10000
MIN_VALUE = -10000


class Agent:
    def __init__(self, tile, game):
        self.tile = tile.upper()
        self.game = game

    def switchTile(self, tile):
        if tile == 'O': return 'X'
        return 'O'

    def getMove(self):
        print("Error: getMove not implemented")

class AlphaBetaAgent(Agent):
    def __init__(self, tile, game, maxDepth):
        super(AlphaBetaAgent, self).__init__(tile, game)
        self.maxDepth = maxDepth

    def getMove(self):
        bestScore, bestMove = self.minimaxDecision(self.game.board)
        return bestMove

    def minimaxDecision(self, board):
        return self.maxValue(board, self.tile, 0, MIN_VALUE, MAX_VALUE)

    def maxValue(self, board, tile, depth, alpha, beta):
        possibleMoves = self.game.getValidMoves(board, tile)
        if len(possibleMoves) == 0 or depth >= self.maxDepth:
            score = self.game.getScoreOfBoard(board)[tile]
            return score, None
        else:
            random.shuffle(possibleMoves)
            bestScore = MIN_VALUE
            bestMove = [0, 0]
            for x, y in possibleMoves:
                dupeBoard = self.game.getBoardCopy(self.game.board)
                self.game.makeMove(dupeBoard, tile, x, y)
                score, _ = self.minValue(dupeBoard, self.switchTile(tile), depth + 1, alpha, beta)
                score = -score
                if self.game.isOnCorner(x, y):
                    return score, [x, y]
                if score > bestScore:
                    bestMove = [x, y]
                    bestScore = score
                if bestScore >= beta:
                    return bestScore, bestMove
                if bestScore > alpha:
                    alpha = bestScore
            return bestScore, bestMove

    def minValue(self, board, tile, depth, alpha, beta):
        possibleMoves = self.game.getValidMoves(board, tile)
        if len(possibleMoves) == 0 or depth >= self.maxDepth:
            score = self.game.getScoreOfBoard(board)[tile]
            return score, None
        else:
            random.shuffle(possibleMoves)
            worstScore = MAX_VALUE
            worstMove = [0, 0]
            for x, y in possibleMoves:
                dupeBoard = self.game.getBoardCopy(self.game.board)
                self.game.makeMove(dupeBoard, tile, x, y)
                score, _ = self.maxValue(dupeBoard, self.switchTile(tile), depth + 1, alpha, beta)
                if self.game.isOnCorner(x, y):
                    continue
                score = -score
                if score < worstScore:
                    worstMove = [x, y]
                    worstScore = score
                if worstScore <= alpha:
                    return worstScore, worstMove
                if worstScore <= beta:
                    beta = worstScore
            return worstScore, worstMove


class MinimaxAgent(Agent):
    def __init__(self, tile, game, maxDepth):
        super(MinimaxAgent, self).__init__(tile, game)
        self.maxDepth = maxDepth

    def getMove(self):
        bestScore, bestMove = self.minimaxDecision(self.game.board)
        return bestMove

    def minimaxDecision(self, board):
        return self.maxValue(board, self.tile, 0)

    def maxValue(self, board, tile, depth):
        possibleMoves = self.game.getValidMoves(board, tile)
        if len(possibleMoves) == 0 or depth >= self.maxDepth:
            score = self.game.getScoreOfBoard(board)[tile]
            return score, None
        else:
            random.shuffle(possibleMoves)
            bestScore = MIN_VALUE
            bestMove = [0,0]
            for x, y in possibleMoves:
                dupeBoard = self.game.getBoardCopy(self.game.board)
                self.game.makeMove(dupeBoard, tile, x, y)
                score, _ = self.minValue(dupeBoard, self.switchTile(tile), depth+1)
                score = -score
                if self.game.isOnCorner(x, y):
                    return score, [x, y]
                if score > bestScore:
                    bestMove = [x, y]
                    bestScore = score
            return bestScore, bestMove


    def minValue(self, board, tile, depth):
        possibleMoves = self.game.getValidMoves(board, tile)
        if len(possibleMoves) == 0 or depth >= self.maxDepth:
            score = self.game.getScoreOfBoard(board)[tile]
            return score, None
        else:
            random.shuffle(possibleMoves)
            worstScore = MAX_VALUE
            worstMove = [0,0]
            for x, y in possibleMoves:
                dupeBoard = self.game.getBoardCopy(self.game.board)
                self.game.makeMove(dupeBoard, tile, x, y)
                score, _ = self.maxValue(dupeBoard, self.switchTile(tile), depth+1)
                if self.game.isOnCorner(x, y):
                    continue
                score = -score
                if score < worstScore:
                    worstMove = [x, y]
                    worstScore = score

            return worstScore, worstMove


class GreedyAgent(Agent):
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
