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
        self.whitetoMove = True
        self.moveLog = []
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # Log Move to show log or undo feature
        self.whitetoMove = not self.whitetoMove

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

    def getChessNotation(self, gs):
        piece = gs.board[self.endRow][self.endCol]
        return piece + ": " + self.getRankFile(self.startRow, self.startCol) + " -> " + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.rowsToRanks[r] + self.colsToFiles[c]