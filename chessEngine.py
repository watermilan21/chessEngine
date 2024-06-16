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