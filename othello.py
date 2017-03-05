import random

class Othello:
    def __init__(self):
        self.board = self.getNewBoard()
        self.resetBoard()

    def drawBoard(self, board):
        # This function prints out the board that it was passed. Returns None.
        HLINE = '  +---+---+---+---+---+---+---+---+'

        print('    1   2   3   4   5   6   7   8')
        print(HLINE)
        for y in range(8):
            print(y+1, end=' ')
            for x in range(8):
                print('| %s' % (board[x][y]), end=' ')
            print('|')
            print(HLINE)

    def resetBoard(self):
        # Blanks out the board it is passed, except for the original starting position.
        for x in range(8):
            for y in range(8):
                self.board[x][y] = ' '

        # Starting pieces:
        self.board[3][3] = 'X'
        self.board[3][4] = 'O'
        self.board[4][3] = 'O'
        self.board[4][4] = 'X'

    def getNewBoard(self):
        # Creates a brand new, blank board data structure.
        board = []
        for i in range(8):
            board.append([' '] * 8)
        return board

    def isValidMove(self, board, tile, xstart, ystart):
        # Returns False if the player's move on space xstart, ystart is invalid.
        # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
        if board[xstart][ystart] != ' ' or not self.isOnBoard(xstart, ystart):
            return False

        board[xstart][ystart] = tile # temporarily set the tile on the board.

        if tile == 'X':
            otherTile = 'O'
        else:
            otherTile = 'X'

        tilesToFlip = []
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection # first step in the direction
            y += ydirection # first step in the direction
            if self.isOnBoard(x, y) and board[x][y] == otherTile:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self.isOnBoard(x, y):
                    continue
                while board[x][y] == otherTile:
                    x += xdirection
                    y += ydirection
                    if not self.isOnBoard(x, y): # break out of while loop, then continue in for loop
                        break
                if not self.isOnBoard(x, y):
                    continue
                if board[x][y] == tile:
                    # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])

        board[xstart][ystart] = ' ' # restore the empty space
        if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
            return False
        return tilesToFlip

    def isOnBoard(self, x, y):
        return x >= 0 and x <= 7 and y >= 0 and y <=7
        # Returns True if the coordinates are located on the board.

    def getBoardWithValidMoves(self, board, tile):
        # Returns a new board with . marking the valid moves the given player can make.
        dupeBoard = self.getBoardCopy(board)

        for x, y in self.getValidMoves(dupeBoard, tile):
         dupeBoard[x][y] = '.'
        return dupeBoard

    def getValidMoves(self, board, tile):
        # Returns a list of [x,y] lists of valid moves for the given player on the given board.
        validMoves = []

        for x in range(8):
            for y in range(8):
                if self.isValidMove(board, tile, x, y) != False:
                    validMoves.append([x, y])
        return validMoves

    def getCopyOfBoardAfterMove(self, board, tile, x, y):
        dupeBoard = self.getBoardCopy(board)
        self.makeMove(dupeBoard, tile, x, y)
        return dupeBoard

    def getScoreOfBoard(self, board):
        # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
        xscore = 0
        oscore = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == 'X':
                    xscore += 1
                if board[x][y] == 'O':
                    oscore += 1
        return {'X':xscore, 'O':oscore}


    def enterPlayerTile(self):
        # Lets the player type which tile they want to be.
        # Returns a list with the player's tile as the first item, and the computer's tile as the second.
        tile = ''
        while not (tile == 'X' or tile == 'O'):
            print('Do you want to be X or O?')
            tile = input().upper()

        # the first element in the list is the player's tile, the second is the computer's tile.
        if tile == 'X':
            return ['X', 'O']
        else:
            return ['O', 'X']


    def whoGoesFirst(self):
        # Randomly choose the player who goes first.
        if random.randint(0, 1) == 0:
            return 'computer'
        else:
            return 'player'

    def cornersHeld(self, board):
        corners = {'O': 0, 'X': 0}
        for x in [0, 7]:
            for y in [0, 7]:
                if board[x][y] == 'O':
                    corners['O'] += 1
                elif board[x][y] == 'X':
                    corners['X'] += 1
        return corners

    def playAgain(self):
        # This function returns True if the player wants to play again, otherwise it returns False.
        print('Do you want to play again? (yes or no)')
        return input().lower().startswith('y')


    def makeMove(self, board, tile, xstart, ystart):
        # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
        # Returns False if this is an invalid move, True if it is valid.
        tilesToFlip = self.isValidMove(board, tile, xstart, ystart)

        if tilesToFlip == False:
            return False

        board[xstart][ystart] = tile
        for x, y in tilesToFlip:
            board[x][y] = tile
        return True


    def getBoardCopy(self, board):
        # Make a duplicate of the board list and return the duplicate.
        dupeBoard = self.getNewBoard()

        for x in range(8):
            for y in range(8):
                dupeBoard[x][y] = board[x][y]

        return dupeBoard


    def isOnCorner(self, x, y):
        # Returns True if the position is in one of the four corners.
        return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


    def getPlayerMove(self, board, playerTile):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
        DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
        while True:
            print('Enter your move, or type quit to end the game, or hints to turn off/on hints.')
            move = input().lower()
            if move == 'quit':
                return 'quit'
            if move == 'hints':
                return 'hints'

            if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
                y = int(move[0]) - 1
                x = int(move[1]) - 1
                if self.isValidMove(board, playerTile, x, y) == False:
                    continue
                else:
                    break
            else:
                print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
                print('For example, 81 will be the top-right corner.')

        return [x, y]


    def getComputerMove(self, board, computerTile):
        # Given a board and the computer's tile, determine where to
        # move and return that move as a [x, y] list.
        possibleMoves = self.getValidMoves(board, computerTile)

        # randomize the order of the possible moves
        random.shuffle(possibleMoves)

        # always go for a corner if available.
        for x, y in possibleMoves:
            if self.isOnCorner(x, y):
                return [x, y]

        bestScore = -1
        for x, y in possibleMoves:
            dupeBoard = self.getBoardCopy(board)
            self.makeMove(dupeBoard, computerTile, x, y)
            score = self.getScoreOfBoard(dupeBoard)[computerTile]
            if score > bestScore:
                bestMove = [x, y]
                bestScore = score
        return bestMove


    def showPoints(self, playerTile, computerTile):
        # Prints out the current score.
        scores = self.getScoreOfBoard(self.board)
        print('Player1 have %s points. Player2 has %s points.' % (scores[playerTile], scores[computerTile]))
