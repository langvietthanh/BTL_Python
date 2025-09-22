import pygame as pg
from MODEL.Piece import *
from MODEL.Chess_Board import *

Pieces = board.pieces
selected_piece = None


class Controller:
    def __init__(self, board, view):
        self.board = board
        self.view = view
        self.selected_piece = None