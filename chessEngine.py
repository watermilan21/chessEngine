"""
Class is responsible for storing info on the current state of the chess game.
Also responsible for determination of legal moves in the current state.
Keeps a move log as well.
"""

# Base Chess Board
class GameState():
    def __init__(self):
        # Board - 8x8 2D-List and each list has 2 characters.
        # The first character represents color of the piece - 'b','w'.
        # The second character represents type of the piece - 'K','Q','R','B','N','P'.
        # "--" represents an empty space.
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                            'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
    
        self.whitetoMove = True
        self.moveLog = []
        self.whiteKingLoc = (7,4)
        self.blackKingLoc = (0,4)
        self.checkMate = False
        self.staleMate = False
    '''
    Takes input as a move and executes it directly (Doesn't work for en passant, castling or pawn promotion)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # Log Move to show log or undo feature
        self.whitetoMove = not self.whitetoMove
        if move.pieceMoved == "wK":
            self.whiteKingLoc = (move.endRow, move.endCol)
        if move.pieceMoved == "bK":
            self.blackKingLoc = (move.endRow, move.endCol)

    def undoMove(self):
        move = self.moveLog.pop()
        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured
        self.whitetoMove = not self.whitetoMove
        if move.pieceMoved == "wK":
            self.whiteKingLoc = (move.startRow, move.startCol)
        if move.pieceMoved == "bK":
            self.blackKingLoc = (move.startRow, move.startCol)

    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        for i in range(len(moves)-1, -1, -1): # Iterate backwards to prevent bugs
            self.makeMove(moves[i])
            self.whitetoMove = not self.whitetoMove
            if self.inCheck():
                moves.remove(moves[i])
                print("Illegal Move")
            self.whitetoMove = not self.whitetoMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves
    
    def inCheck(self):
        if self.whitetoMove:
            return self.squareUnderAttack(self.whiteKingLoc[0],self.whiteKingLoc[1])
        else:
            return self.squareUnderAttack(self.blackKingLoc[0],self.blackKingLoc[1])

    def squareUnderAttack(self, r, c):
        self.whitetoMove = not self.whitetoMove
        oppMoves = self.getAllPossibleMoves()
        self.whitetoMove = not self.whitetoMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True

    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                turn = self.board[r][c][0]
                piece = self.board[r][c][1]
                if (turn == 'w' and self.whitetoMove) or (turn == 'b' and not self.whitetoMove):
                    self.moveFunctions[piece](r,c, moves)
        return moves

    '''
    Used to get all available PAWN moves.
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whitetoMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c), (r-1,c), self.board))
                if self.board[r-2][c] == "--" and r == 6:
                    moves.append(Move((r,c), (r-2,c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r,c), (r-1,c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r,c), (r-1,c+1), self.board))

        if not self.whitetoMove:
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1,c), self.board))
                if self.board[r+2][c] == "--" and r == 1:
                    moves.append(Move((r,c), (r+2,c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r,c), (r+1,c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r,c), (r+1,c+1), self.board))
    '''
    Used to get all ROOK moves.
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1,0),(1,0),(0,-1),(0,1))
        enemyColor = "b" if self.whitetoMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else:
                        break
                else:
                    break
    '''
    Used to get all KNIGHT moves.
    '''
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2,-1),(-2,1),(2,-1),(2,1),(1,2),(1,-2),(-1,2),(-1,-2))
        allyColor = "w" if self.whitetoMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))
    '''
    Used to get all BISHOP moves.
    '''
    def getBishopMoves(self, r, c, moves):
        directions = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemyColor = "b" if self.whitetoMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else:
                        break
                else:
                    break
    '''
    Used to get all QUEEN moves.
    '''
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
    '''
    Used to get all KING moves.
    '''
    def getKingMoves(self, r, c, moves):
        directions = ((1,1),(1,-1),(1,0),(0,1),(0,-1),(-1,-1),(-1,0),(-1,1))
        allyColor = "w" if self.whitetoMove else "b"
        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))


class Move():
    # Assigning dictionaries for ranks and files to index values
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        # Setting values for ease of use
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self, gs):
        piece = gs.board[self.endRow][self.endCol]
        return piece + ": " + self.getRankFile(self.startRow, self.startCol) + " -> " + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.rowsToRanks[r] + self.colsToFiles[c]