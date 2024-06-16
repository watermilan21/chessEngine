'''
Main file for handling user input and displaying current GameState
'''

import pygame as p
import sys
sys.path.insert(1,"C:\\Users\\milan\\OneDrive\\Documents\\GitHub\\chessEngine\\chessEngine.py")
import chessEngine

p.init()
width = height = 512
dimension = 8
sq_size = height // dimension
max_fps = 15
images = {}

'''
Initialize global dictionary of images.
This will be called exactly once in the main.
'''
def loadImages():
    pieces = ['wp','wR','wN','wB','wQ','wK','bp','bR','bN','bB','bQ','bK']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(sq_size, sq_size))
    # We can access an image by saying 'images['wp']
    # pieces = IMAGES['wp'] = p.image.load("images/wp.png")  --> Not Efficient, but Possible.

'''
The main driver for our code. This will handle user input and updating graphics.
'''

def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    gs = chessEngine.GameState()
    # print(gs.board)
    loadImages() # ONLY DO THIS ONCE!
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(max_fps)
        p.display.flip()

'''
Responsible for all graphics within the current game state.
'''
def drawGameState(screen,gs):
    drawBoard(screen, gs.board) # Draws the square on the board.
    drawPieces(screen, gs.board) # Draws pieces on top of the squares

# Draws squares on the board.
def drawBoard(screen, board):
    colors = [p.Color("white"),p.Color("gray")]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*sq_size,r*sq_size,sq_size,sq_size))


#Draws pieces on the board.
def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*sq_size,r*sq_size,sq_size,sq_size))


if __name__ == "__main__":
    main()