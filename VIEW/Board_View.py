import pygame as pg
from MODEL.Piece import *

# Color for cell
WHITE = (238, 238, 210)
DARKGREEN = (118, 150, 86)
cell_size = 100
# -------------------------------------------------------------------------------------------

class Board_View:
    def __init__(self,screen,board):
        self.screen = screen
        self.board = board

    def init_piece(self):
        # Black piece
        # Rook
        img_black_rook = pg.image.load("PNG/black_rook.png")
        piece_black_LeftRook = Piece(img_black_rook, "Black", "rook", 0, 0, self.board)
        piece_black_RightRook = Piece(img_black_rook, "Black", "rook", 7, 0, self.board)
        # Knight
        img_black_knight = pg.image.load("PNG/black_knight.png")
        piece_black_LeftKnight = Piece(img_black_knight, "Black", "knight", 1, 0, self.board)
        piece_black_RightKnight = Piece(img_black_knight, "Black", "knight", 6, 0, self.board)
        # Bishop
        img_black_bishop = pg.image.load("PNG/black_bishop.png")
        piece_black_LeftBishop = Piece(img_black_bishop, "Black", "bishop", 2, 0, self.board)
        piece_black_RightBishop = Piece(img_black_bishop, "Black", "bishop", 5, 0, self.board)
        # Queen
        img_black_queen = pg.image.load("PNG/black_queen.png")
        piece_black_Queen = Piece(img_black_queen, "Black", "queen", 3, 0, self.board)
        # King
        img_black_king = pg.image.load("PNG/black_king.png")
        piece_black_King = Piece(img_black_king, "Black", "king", 4, 0, self.board)
        # Pawn
        piece_black_pawn = []
        img_black_rook = pg.image.load("PNG/black_pawn.png")
        for x_i in range(8):
            pawn = Piece(img_black_rook, "Black", "pawn", x_i, 1, self.board)
            piece_black_pawn.append(pawn)

        # White piece
        # Rook
        img_white_rook = pg.image.load("PNG/white_rook.png")
        piece_white_LeftRook = Piece(img_white_rook, "White", "rook", 0, 7, self.board)
        piece_white_RightRook = Piece(img_white_rook, "White", "rook", 7, 7, self.board)
        # Knight
        img_white_knight = pg.image.load("PNG/white_knight.png")
        piece_white_LeftKnight = Piece(img_white_knight, "White", "knight", 1, 7, self.board)
        piece_white_RightKnight = Piece(img_white_knight, "White", "knight", 6, 7, self.board)
        # Bishop
        img_white_bishop = pg.image.load("PNG/white_bishop.png")
        piece_white_LeftBishop = Piece(img_white_bishop, "White", "bishop", 2, 7, self.board)
        piece_white_RightBishop = Piece(img_white_bishop, "White", "bishop", 5, 7, self.board)
        # Queen
        img_white_queen = pg.image.load("PNG/white_queen.png")
        piece_white_Queen = Piece(img_white_queen, "White", "queen", 3, 7, self.board)
        # King
        img_white_king = pg.image.load("PNG/white_king.png")
        piece_white_King = Piece(img_white_king, "White", "king", 4, 7, self.board)
        # Pawn
        piece_white_pawn = []
        img_white_rook = pg.image.load("PNG/white_pawn.png")
        for x_i in range(8):
            pawn = Piece(img_white_rook, "White", "pawn", x_i, 6, self.board)
            piece_white_pawn.append(pawn)
        # Black piece
        self.board.add_piece(piece_black_LeftRook)
        self.board.add_piece(piece_black_LeftKnight)
        self.board.add_piece(piece_black_LeftBishop)
        self.board.add_piece(piece_black_Queen)
        self.board.add_piece(piece_black_King)
        self.board.add_piece(piece_black_RightRook)
        self.board.add_piece(piece_black_RightKnight)
        self.board.add_piece(piece_black_RightBishop)
        for Pawn in piece_black_pawn:
            self.board.add_piece(Pawn)

        # White piece
        self.board.add_piece(piece_white_LeftRook)
        self.board.add_piece(piece_white_LeftKnight)
        self.board.add_piece(piece_white_LeftBishop)
        self.board.add_piece(piece_white_Queen)
        self.board.add_piece(piece_white_King)
        self.board.add_piece(piece_white_RightRook)
        self.board.add_piece(piece_white_RightKnight)
        self.board.add_piece(piece_white_RightBishop)
        for Pawn in piece_white_pawn:
            self.board.add_piece(Pawn)

    def draw(self):
        for r in range(8):
            for c in range(8):
                color = WHITE if (r + c) % 2 == 0 else DARKGREEN
                pygame.draw.rect(self.screen, color, (r * cell_size, c * cell_size, cell_size, cell_size))
        for p in self.board.pieces:
            self.screen.blit(p.img, p.rect)
        pg.display.flip()