import pygame as pg
import sys, os
from pygame.locals import *
from Chess_Board import *
from Piece import *

pygame.init()

window_height,window_width  = 800,800
img_height,img_width = 60,60

screen = pygame.display.set_mode((window_height,window_width))
pygame.display.set_caption("CHESS_BOARD")

# Board
board = Board()
board.Build_Board(screen)

# Piece
# Rook
img_black_rook = pg.image.load("PNG/black_rook.png")
img_white_rook = pg.image.load("PNG/white_rook.png")
# Knight
img_black_knight = pg.image.load("PNG/black_knight.png")
img_white_knight = pg.image.load("PNG/white_knight.png")
# Bishop
img_black_bishop = pg.image.load("PNG/black_bishop.png")
img_white_bishop = pg.image.load("PNG/white_bishop.png")
# Queen
img_black_queen = pg.image.load("PNG/black_queen.png")
img_white_queen = pg.image.load("PNG/white_queen.png")
# King
img_black_king = pg.image.load("PNG/black_king.png")
img_white_king = pg.image.load("PNG/white_king.png")
# Pawn
piece_black_pawn = []
piece_white_pawn = []
img_black_pawn = pg.image.load("PNG/black_pawn.png")
img_white_pawn = pg.image.load("PNG/white_pawn.png")

while True :
# ---------------------------------------------------------------------------------------------------------------------
    for x_i in range(8):
        pawn = Piece(img_white_pawn, "White", "rook", x_i, 6,screen)
        piece_white_pawn.append(pawn)
    for x_i in range(8):
        pawn = Piece(img_black_pawn, "Black", "rook", x_i, 1,screen)
        piece_black_pawn.append(pawn)
    piece_black_LeftRook = Piece(img_black_rook, "Black", "rook", 0, 0,screen)
    piece_black_RightRook = Piece(img_black_rook, "Black", "rook", 7, 0,screen)
    piece_black_LeftKnight = Piece(img_black_knight, "Black", "knight", 1, 0,screen)
    piece_black_RightKnight = Piece(img_black_knight, "Black", "knight", 6, 0,screen)
    piece_black_LeftBishop = Piece(img_black_bishop, "Black", "bishop", 2, 0,screen)
    piece_black_RightBishop = Piece(img_black_bishop, "Black", "bishop", 5, 0,screen)
    piece_black_Queen = Piece(img_black_queen, "Black", "queen", 3, 0,screen)
    piece_black_King = Piece(img_black_king, "Black", "king", 4, 0,screen)

    piece_white_LeftRook = Piece(img_white_rook, "White", "rook", 0, 7,screen)
    piece_white_RightRook = Piece(img_white_rook, "White", "rook", 7, 7,screen)
    piece_white_LeftKnight = Piece(img_white_knight, "White", "knight", 1, 7,screen)
    piece_white_RightKnight = Piece(img_white_knight, "White", "knight", 6, 7,screen)
    piece_white_LeftBishop = Piece(img_white_bishop, "White", "bishop", 2, 7,screen)
    piece_white_RightBishop = Piece(img_white_bishop, "White", "bishop", 5, 7,screen)
    piece_white_Queen = Piece(img_white_queen, "White", "queen", 3, 7,screen)
    piece_white_King = Piece(img_white_king, "White", "king", 4, 7,screen)
# ---------------------------------------------------------------------------------------------------------------------
    piece_white_LeftRook.set_coordinate(0,5)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

