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
board.build_board(screen)

# Black piece
# Rook
img_black_rook = pg.image.load("PNG/black_rook.png")
piece_black_LeftRook = Piece(img_black_rook, "Black", "rook", 0, 0)
piece_black_RightRook = Piece(img_black_rook, "Black", "rook", 7, 0)
# Knight
img_black_knight = pg.image.load("PNG/black_knight.png")
piece_black_LeftKnight = Piece(img_black_knight, "Black", "knight", 1, 0)
piece_black_RightKnight = Piece(img_black_knight, "Black", "knight", 6, 0)
# Bishop
img_black_bishop = pg.image.load("PNG/black_bishop.png")
piece_black_LeftBishop = Piece(img_black_bishop, "Black", "bishop", 2, 0)
piece_black_RightBishop = Piece(img_black_bishop, "Black", "bishop", 5, 0)
# Queen
img_black_queen = pg.image.load("PNG/black_queen.png")
piece_black_Queen = Piece(img_black_queen, "Black", "queen", 3, 0)
# King
img_black_king = pg.image.load("PNG/black_king.png")
piece_black_King = Piece(img_black_king, "Black", "king", 4, 0)
# Pawn
piece_black_pawn = []
img_black_rook = pg.image.load("PNG/black_pawn.png")
for x_i in range(8):
    pawn = Piece(img_black_rook, "Black", "rook", x_i, 1)
    piece_black_pawn.append(pawn)

# White piece
# Rook
img_white_rook = pg.image.load("PNG/white_rook.png")
piece_white_LeftRook = Piece(img_white_rook, "White", "rook", 0, 7)
piece_white_RightRook = Piece(img_white_rook, "White", "rook", 7, 7)
# Knight
img_white_knight = pg.image.load("PNG/white_knight.png")
piece_white_LeftKnight = Piece(img_white_knight, "White", "knight", 1, 7)
piece_white_RightKnight = Piece(img_white_knight, "White", "knight", 6, 7)
# Bishop
img_white_bishop = pg.image.load("PNG/white_bishop.png")
piece_white_LeftBishop = Piece(img_white_bishop, "White", "bishop", 2, 7)
piece_white_RightBishop = Piece(img_white_bishop, "White", "bishop", 5, 7)
# Queen
img_white_queen = pg.image.load("PNG/white_queen.png")
piece_white_Queen = Piece(img_white_queen, "White", "queen", 3, 7)
# King
img_white_king = pg.image.load("PNG/white_king.png")
piece_white_King = Piece(img_white_king, "White", "king", 4, 7)
# Pawn
piece_white_pawn = []
img_white_rook = pg.image.load("PNG/white_pawn.png")
for x_i in range(8):
    pawn = Piece(img_white_rook, "White", "rook", x_i, 6)
    piece_white_pawn.append(pawn)


while True :
    # Show black piece
    piece_black_LeftRook.show_piece(screen)
    piece_black_LeftKnight.show_piece(screen)
    piece_black_LeftBishop.show_piece(screen)
    piece_black_RightRook.show_piece(screen)
    piece_black_RightKnight.show_piece(screen)
    piece_black_RightBishop.show_piece(screen)
    piece_black_Queen.show_piece(screen)
    piece_black_King.show_piece(screen)
    for pawn in piece_black_pawn:
        pawn.show_piece(screen)
    # Show white piece
    piece_white_LeftRook.show_piece(screen)
    piece_white_LeftKnight.show_piece(screen)
    piece_white_LeftBishop.show_piece(screen)
    piece_white_RightRook.show_piece(screen)
    piece_white_RightKnight.show_piece(screen)
    piece_white_RightBishop.show_piece(screen)
    piece_white_Queen.show_piece(screen)
    piece_white_King.show_piece(screen)
    for pawn in piece_white_pawn:
        pawn.show_piece(screen)
    # ---------------------------------------
    piece_white_LeftRook.set_coordinate(0,5)
    piece_white_LeftRook.show_piece(screen)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

