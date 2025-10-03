from MODEL.Chess_Board import *
import pygame
cell_size=100

# role = pawn, bishop, knight, rook, queen, king
# offset : khoảng cách tọa độ chuột với góc trên trái
# current_coordinates : Tọa độ hiện tại của quân cờ
# before_coordinates : Tọa độ trước đó của quân cờ

# Quân đen sẽ đi theo valid_move, quân trắng thì chỉ cần nhân -1

class Piece:
    def __init__(self,img,color,role,x,y):
        self.color = color
        self.role = role
        self.offset = [0,0]
        self.current_coordinates = [x,y]
        self.before_coordinates = [x,y]
        self.img = pygame.transform.scale(img,(100,100))
        self.rect = self.img.get_rect(topleft = (self.current_coordinates[0] * cell_size ,self.current_coordinates[1] * cell_size))
        self.valid_moves = []
        self.replaced_by = []

    # đặt lại tọa độ
    def set_coordinate(self,x,y):
        # chỉ set lại tọa độ khi thực sự di chuyển quân
        if [x, y] == self.current_coordinates:
            self.set_rect()
            return
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

        elif self.role == 'rook':
            self.set_rook_moves(board)

        elif self.role == 'knight':
            self.set_knight_moves(board)

        elif self.role == 'bishop':
            self.set_bishop_moves(board)

        elif self.role == 'queen':
            self.set_queen_moves(board)

        elif self.role == 'king':
            self.set_king_moves(board)

    def set_pawn_moves(self,board):
        pawn_steps = [[0, 1], [1, 1], [-1, 1]]
        if self.current_coordinates == self.before_coordinates : pawn_steps.append([0,2])
        for step in pawn_steps:
            if self.color == 'Black':
                next_move = [step[0] + self.current_coordinates[0], step[1] + self.current_coordinates[1]]
            else :
                next_move = [-step[0] + self.current_coordinates[0], -step[1] + self.current_coordinates[1]]

            if 0 <= next_move[0] <= 7 and 0 <= next_move[1] <= 7 :
                # Nước đi khi có cơ hội ăn quân địch chéo
                if next_move[0] != self.current_coordinates[0]:
                    if self.color == 'Black':
                        if board.cell_have_white_piece(next_move[0], next_move[1]):
                            self.valid_moves.append(next_move)
                        elif board.cell_have_black_piece(next_move[0], next_move[1]):
                            piece = board.get_piece_with_coordinates(next_move[0],next_move[1])
                            piece.replaced_by.append(self)

                    if self.color == 'White':
                        if board.cell_have_black_piece(next_move[0], next_move[1]):
                            self.valid_moves.append(next_move)
                        elif board.cell_have_white_piece(next_move[0], next_move[1]):
                            piece = board.get_piece_with_coordinates(next_move[0], next_move[1])
                            piece.replaced_by.append(self)

                # Ô trước phải trống => next_move không nằm trong tọa độ hiện tại của các quân có trên bàn cờ
                elif board.cell_is_empty(next_move[0], next_move[1]):
                    self.valid_moves.append(next_move)

    def set_rook_moves(self, board):
        rook_steps = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for step in rook_steps:
            x, y = self.current_coordinates[0] + step[0], self.current_coordinates[1] + step[1]
            while 0 <= x <= 7 and 0 <= y <= 7:
                if self.color == 'White':
                    if board.cell_have_black_piece(x, y):
                        self.valid_moves.append([x, y])
                        break
                    elif board.cell_have_white_piece(x, y):
                        piece = board.get_piece_with_coordinates(x,y)
                        piece.replaced_by.append(self)
                        break

                if self.color == 'Black':
                    if board.cell_have_white_piece(x, y):
                        self.valid_moves.append([x, y])
                        break
                    elif board.cell_have_black_piece(x, y):
                        piece = board.get_piece_with_coordinates(x, y)
                        piece.replaced_by.append(self)
                        break

                if board.cell_is_empty(x, y):
                    self.valid_moves.append([x, y])

                x, y = x + step[0], y + step[1]

    def set_knight_moves(self, board) :
        knight_steps = [[1, 2], [1, -2], [2, 1], [2, -1], [-1, 2], [-1, -2], [-2, 1], [-2, -1]]
        for step in knight_steps:
            next_move = [step[0] + self.current_coordinates[0], step[1] + self.current_coordinates[1]]

            if 0 <= next_move[0] <= 7 and 0 <= next_move[1] <= 7 :
                # Nước đi khi có cơ hội ăn quân địch
                if self.color == 'Black':

                    if board.cell_have_white_piece(next_move[0], next_move[1]):
                        self.valid_moves.append(next_move)

                    elif board.cell_have_black_piece(next_move[0], next_move[1]):
                        piece = board.get_piece_with_coordinates(next_move[0], next_move[1])
                        piece.replaced_by.append(self)
                    
                elif self.color == 'White':

                    if board.cell_have_black_piece(next_move[0], next_move[1]):
                        self.valid_moves.append(next_move)

                    elif board.cell_have_white_piece(next_move[0], next_move[1]):
                        piece = board.get_piece_with_coordinates(next_move[0], next_move[1])
                        piece.replaced_by.append(self)
                    
                # Ô trước phải trống => next_move không nằm trong tọa độ hiện tại của các quân có trên bàn cờ
                if board.cell_is_empty(next_move[0], next_move[1]):
                    self.valid_moves.append(next_move)

    def set_bishop_moves(self, board):
        bishop_steps = [[1,1],[-1,-1],[-1,1],[1,-1]]
        for step in bishop_steps:
            x , y = self.current_coordinates[0] + step[0], self.current_coordinates[1] + step[1]

            while 0 <= x <= 7 and 0 <= y <= 7 :
                if self.color == 'White':
                    if board.cell_have_black_piece(x, y):
                        self.valid_moves.append([x,y])
                        break
                    elif board.cell_have_white_piece(x, y):
                        piece = board.get_piece_with_coordinates(x, y)
                        piece.replaced_by.append(self)
                        break

                if self.color == 'Black':

                    if board.cell_have_white_piece(x, y):
                        self.valid_moves.append([x, y])
                        break
                    elif board.cell_have_black_piece(x, y):
                        piece = board.get_piece_with_coordinates(x, y)
                        piece.replaced_by.append(self)
                        break

                if board.cell_is_empty(x, y):
                    self.valid_moves.append([x, y])

                x, y = x + step[0], y + step[1]

    def set_queen_moves(self, board):
        # kết hợp của rook_move và bishop move
        self.set_bishop_moves(board)
        self.set_rook_moves(board)

    def set_pawn_moves_case_king(self, board, predict_move):
        pawn_steps = [[1, 1], [-1, 1]]
        for step in pawn_steps:
            if self.color == 'Black':
                next_move = [step[0] + self.current_coordinates[0], step[1] + self.current_coordinates[1]]
            else:
                next_move = [-step[0] + self.current_coordinates[0], -step[1] + self.current_coordinates[1]]
            if 0 <= next_move[0] <= 7 and 0 <= next_move[1] <= 7:
                # Nước đi khi có cơ hội ăn vua địch (chéo)
                piece = board.get_piece_with_coordinates(next_move[0], next_move[1])
                if piece is None:
                    predict_move.append(next_move)

    def set_king_moves(self, board):
        king_valid_steps = [[x, y] for x in range(-1, 2) for y in range(-1, 2) if (x != 0 or y != 0)]
        warning_moves = board.predict_moves

        for step in king_valid_steps:
            next_move = [step[0] + self.current_coordinates[0], step[1] + self.current_coordinates[1]]
            if (0 <= next_move[0] <= 7) and (0 <= next_move[1] <= 7):
                piece = board.get_piece_with_coordinates(next_move[0], next_move[1])
                # Nước đi khi có cơ hội ăn quân địch chéo
                if None != piece:
                    if self.color == 'Black':
                        if board.cell_have_white_piece(next_move[0], next_move[1]) and len(piece.replaced_by) == 0:
                            self.valid_moves.append(next_move)
                        elif board.cell_have_black_piece(next_move[0], next_move[1]):
                            piece.replaced_by.append(self)

                    if self.color == 'White':
                        if board.cell_have_black_piece(next_move[0], next_move[1]) and len(piece.replaced_by) == 0 :
                            self.valid_moves.append(next_move)
                        elif board.cell_have_white_piece(next_move[0], next_move[1]):
                            piece.replaced_by.append(self)

                # warning_moves được tính từ lúc ấn vào king
                elif next_move not in warning_moves:
                    self.valid_moves.append(next_move)

    def had_move(self):
        return self.current_coordinates != self.before_coordinates


