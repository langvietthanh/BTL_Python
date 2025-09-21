import pygame as pg
from Piece import *

WHITE = (238, 238, 210)
DARKGREEN = (118, 150, 86)
cell_size = 100

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
# -------------------------------------------------------------------------------------------
class Board:
    def __init__(self):
        self.pieces = []

    def init_piece(self):
        # Black piece
        self.add_piece(piece_black_LeftRook)
        self.add_piece(piece_black_LeftKnight)
        self.add_piece(piece_black_LeftBishop)
        self.add_piece(piece_black_Queen)
        self.add_piece(piece_black_King)
        self.add_piece(piece_black_RightRook)
        self.add_piece(piece_black_RightKnight)
        self.add_piece(piece_black_RightBishop)
        for Pawn in piece_black_pawn:
            self.add_piece(Pawn)

        # Show white piece
        self.add_piece(piece_white_LeftRook)
        self.add_piece(piece_white_LeftKnight)
        self.add_piece(piece_white_LeftBishop)
        self.add_piece(piece_white_Queen)
        self.add_piece(piece_white_King)
        self.add_piece(piece_white_RightRook)
        self.add_piece(piece_white_RightKnight)
        self.add_piece(piece_white_RightBishop)
        for Pawn in piece_white_pawn:
            self.add_piece(Pawn)

    def add_piece(self,piece):
        self.pieces.append(piece)

    def remove_piece (self,piece):
        self.pieces.remove(piece)

    def build_board(self,screen):
        for r in range(8):
            for c in range(8):
#               if i + j % 2 == 0 : white cell
#               else green cell
                color = WHITE if (r + c) % 2 == 0 else DARKGREEN
                pygame.draw.rect(screen, color, (r * cell_size, c * cell_size, cell_size, cell_size))
        for p in self.pieces:
            p.show_piece(screen)


