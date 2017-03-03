
import sys
from othello import Othello

print('Welcome to Reversi!')

while True:
    game = Othello()

    # Reset the board and game.
    game.resetBoard()
    playerTile, computerTile = game.enterPlayerTile()
    turn = game.whoGoesFirst()
    print('The ' + turn + ' will go first.')

    while True:
        if turn == 'player':
            # Player's turn.
            game.drawBoard(game.board)
            game.showPoints(playerTile, computerTile)
            move = game.getPlayerMove(game.board, playerTile)
            if move == 'quit':
                print('Thanks for playing!')
                sys.exit() # terminate the program
            else:
                game.makeMove(game.board, playerTile, move[0], move[1])
            if game.getValidMoves(game.board, computerTile) == []:
                break
            else:
                turn = 'computer'

        else:
            # Computer's turn.
            game.drawBoard(game.board)
            game.showPoints(playerTile, computerTile)
            input('Press Enter to see the computer\'s move.')
            x, y = game.getComputerMove(game.board, computerTile)
            game.makeMove(game.board, computerTile, x, y)

            if game.getValidMoves(game.board, playerTile) == []:
                break
            else:
                turn = 'player'

    # Display the final score.
    game.drawBoard(game.board)
    scores = game.getScoreOfBoard(game.board)
    print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))
    if scores[playerTile] > scores[computerTile]:
        print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
    else:
        print('The game was a tie!')

    if not game.playAgain():
        break



