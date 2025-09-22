import pygame
from MODEL.Chess_Board import *
cell_size=100

# role = pawn, bishop, knight, rook, queen, king
# offset : khoảng cách tọa độ chuột với góc trên trái
# current_coordinates : Tọa độ hiện tại của quân cờ
# before_coordinates : Tọa độ trước đó của quân cờ

# Quân đen sẽ đi theo valid_move, quân trắng thì chỉ cần nhân -1

pawn_valid_move = [[0,1],[1,1],[-1,1]]
# rook_valid_move = []
# knight_valid_move = [[0,-1],[-1,0],[0,1]]
# bishop_valid_move = [[0,-1],[1,0],[0,1]]
# queen_valid_move = [[0,-1],[1,1],[0,1]]
# king_valid_move = [[0,-1],[1,0],[0,1]]

class Piece:
    def __init__(self,img,color,role,x,y,board):
        self.color = color
        self.role = role
        self.offset = [0,0]
        self.current_coordinates = [x,y]
        self.before_coordinates = [x,y]
        self.img = pygame.transform.scale(img,(100,100))
        self.rect = self.img.get_rect(topleft = (self.current_coordinates[0] * cell_size ,
                                                 self.current_coordinates[1] * cell_size))
        self.valid_moves = None

    # đặt lại tọa độ
    def set_coordinate(self,x,y,board):
        self.before_coordinates = self.current_coordinates
        self.current_coordinates = [x,y]
        self.set_rect()

    def set_rect(self):
        self.rect.x = self.current_coordinates[0] * cell_size
        self.rect.y = self.current_coordinates[1] * cell_size

    def set_valid_moves(self,board):
        self.valid_moves = []
        # valid move thay đổi liên tục => xác định qua vị trí hiện tại
        if self.role == 'pawn':
            self.set_pawn_moves(board)

        # elif self.role == 'rook':
        #     self.set_rook_moves(board, valid_coordinates)
        #     return valid_coordinates
        # elif self.role == 'kinght':
        # elif self.role == 'bishop':
        # elif self.role == 'queen':
        # elif self.role == 'king':

    def set_pawn_moves(self,board):
        for co in pawn_valid_move:
            if self.color == 'Black':
                future_coordinates = [co[0] + self.current_coordinates[0], co[1] + self.current_coordinates[1]]
            else :
                future_coordinates = [-co[0] + self.current_coordinates[0], -co[1] + self.current_coordinates[1]]

            if 0 <= future_coordinates[0] <= 7 and 0 <= future_coordinates[1] <= 7 :
                # Nước đi khi có cơ hội ăn quân địch chéo
                if future_coordinates[0] != self.current_coordinates[0]:
                    if (self.color == 'Black') and (future_coordinates in board.all_coordinates_of_white):
                        self.valid_moves.append(future_coordinates)
                    if (self.color == 'White') and (future_coordinates in board.all_coordinates_of_black):
                        self.valid_moves.append(future_coordinates)
                # Ô trước phải trống => future_coordinates không nằm trong tọa độ hiện tại của các quân có trên bàn cờ
                # elif future_coordinates not in board.all_coordinates_of_white and future_coordinates not in board.all_coordinates_of_black:
                elif future_coordinates not in (board.all_coordinates_of_white + board.all_coordinates_of_black):
                    self.valid_moves.append(future_coordinates)

    # def set_rook_moves(self, board, valid_coordinates):
