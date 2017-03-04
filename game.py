
import sys
from othello import Othello
from agents import MinimaxAgent, GreedyAgent, AlphaBetaAgent
import numpy as np
import time

print('Welcome to Reversi!')

epoch = 0
maxEpoch = 20
game = Othello()

game.resetBoard()
tile1, tile2 = 'O', 'X'
agent1 = GreedyAgent(tile1, game)
# agent2 = GreedyAgent(tile2, game)
# agent1 = MinimaxAgent(tile1, game, 2)
# agent2 = MinimaxAgent(tile2, game, 2)
# agent1 = AlphaBetaAgent(tile1, game, 4)
agent2 = AlphaBetaAgent(tile2, game, 4)
render = False
score1 = []
score2 = []

start = time.time()
#Start a new round
while True:
    game.resetBoard()
    roundStartTurn = 'player'
    while True:
        if roundStartTurn == 'computer':
            turn = 'computer'
            roundStartTurn = 'player'
        else:
            turn = 'player'
            roundStartTurn = 'computer'

        if render:
            game.drawBoard(game.board)
            game.showPoints(tile1, tile2)
        if turn == 'player1':
            # Player's turn.
            move = game.getPlayerMove(game.board, tile1)
            if move == 'quit':
                print('Thanks for playing!')
                sys.exit() # terminate the program
            else:
                game.makeMove(game.board, tile1, move[0], move[1])
            if game.getValidMoves(game.board, tile2) == []:
                break
            else:
                turn = 'computer'
        elif turn == 'player':
            # Computer1's turn.
            # input('Press Enter to see the computer\'s move.')
            x, y = agent1.getMove()
            game.makeMove(game.board, tile1, x, y)
            if game.getValidMoves(game.board, tile2) == []:
                break
            else:
                turn = 'computer'
        else:
            # Computer's turn.
            # input('Press Enter to see the computer\'s move.')
            x, y = agent2.getMove()
            game.makeMove(game.board, tile2, x, y)
            if game.getValidMoves(game.board, tile1) == []:
                break
            else:
                turn = 'player'

    # Display the final score.
    scores = game.getScoreOfBoard(game.board)

    if render:
        game.drawBoard(game.board)
        print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))

    score1.append(scores['X'])
    score2.append(scores['O'])

    epoch += 1
    print('Epoch #', epoch)
    print('Agent1 score:', scores['X'])
    print('Agent2 score:', scores['O'])
    print()
    if epoch > maxEpoch:
        break

print('Agent1 average score:', np.mean(score1))
print('Agent2 average score:', np.mean(score2))
end = time.time()
print('Time: ', end - start)


