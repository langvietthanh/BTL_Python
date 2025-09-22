import pygame as pg
from MODEL.Piece import *


class Board:
    def __init__(self):
        self.pieces = []

    def add_piece(self,piece):
        self.pieces.append(piece)

    def remove_piece (self,piece):
        self.pieces.remove(piece)


