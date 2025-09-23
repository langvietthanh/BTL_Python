import pygame as pg
from MODEL.Piece import *

# pieces = [] : lưu quân cờ trên bàn
# current_coordinates_of_black = [] : lưu toàn bộ tọa độ hiện tại của quân cờ đen
# current_coordinates_of_white = [] : lưu toàn bộ tọa độ hiện tại của quân cờ trắng

class Board:
    def __init__(self):
        self.pieces = []
        self.current_coordinates_of_black = []
        self.current_coordinates_of_white = []
        self.coordinates_can_replace = []

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
        self.current_coordinates_of_black = []
        self.current_coordinates_of_white = []
        for piece in self.pieces:
            if piece.color == 'Black':
                self.current_coordinates_of_black.append(piece.current_coordinates)
            else :
                self.current_coordinates_of_white.append(piece.current_coordinates)

    def cell_is_white_piece(self, x, y):
        return [x,y] in self.current_coordinates_of_white

    def cell_is_black_piece(self, x, y):
        return [x,y] in self.current_coordinates_of_black

    def cell_is_empty(self, x, y):
        return ([x,y] not in self.current_coordinates_of_white) and ([x, y] not in self.current_coordinates_of_black)

    def update_all_coordinates_eat(self,selected_piece):
        if selected_piece.role == 'king':
            color = ""
            if selected_piece.color == 'Black': color = "White"
            else : color = "Black"
            # Dự đoán nước đi của quân có thể ăn được quân khac mau
            for piece in self.pieces:
                if piece.color == color:
                    if piece.role != 'pawn':
                        piece.set_valid_moves(self)
                        self.coordinates_can_replace += piece.valid_moves
                    else:
                        if color == "Black": step = [[1,1],[-1,1]]
                        else : step = [[-1,-1],[1,-1]]
                        self.coordinates_can_replace += [piece.current_coordinates[0] + step[0][0],piece.current_coordinates[1] + step[0][1]]
                        self.coordinates_can_replace += [piece.current_coordinates[0] + step[1][0],piece.current_coordinates[1] + step[1][1]]
