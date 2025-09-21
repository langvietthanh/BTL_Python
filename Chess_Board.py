import pygame
from Piece import *

WHITE = (238, 238, 210)
DARKGREEN = (118, 150, 86)
cell_size = 100
class Board:
    def __init__(self):
        self.pieces = []

    def add_piece(self,piece):
        self.pieces.append(piece)

    def remove_piece (self,piece):
        self.pieces.remove(piece)

    def build_board(self,screen):
        for r in range(8):
            for c in range(8):
#               if( i+j % 2 == 0 ) : white cell
#               else green cell
                color = WHITE if (r + c) % 2 == 0 else DARKGREEN
                pygame.draw.rect(screen, color, (r * cell_size, c * cell_size, cell_size, cell_size))
        for p in  self.pieces:
            p.show_piece(screen)





