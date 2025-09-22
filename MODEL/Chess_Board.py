import pygame as pg
from MODEL.Piece import *

# pieces = [] : lưu quân cờ trên bàn
# all_coordinates_of_black = [] : lưu toàn bộ tọa độ hiện tại của quân cờ đen
# all_coordinates_of_white = [] : lưu toàn bộ tọa độ hiện tại của quân cờ trắng

class Board:
    def __init__(self):
        self.pieces = []
        self.all_coordinates_of_black = []
        self.all_coordinates_of_white = []

    def get_piece_with_coordinates(self,x,y):
        for piece in self.pieces:
            if piece.current_coordinates == [x,y]:
                return piece
        return None

    def add_piece(self,piece):
        self.pieces.append(piece)
        self.update_all_coordinates()

    def remove_piece (self,piece):
        self.pieces.remove(piece)
        self.update_all_coordinates()

    def update_all_coordinates(self):
        self.all_coordinates_of_black = []
        self.all_coordinates_of_white = []
        for piece in self.pieces:
            if piece.color == 'Black':
                self.all_coordinates_of_black.append(piece.current_coordinates)
            else :
                self.all_coordinates_of_white.append(piece.current_coordinates)