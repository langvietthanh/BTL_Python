import pygame as pg
from MODEL.Piece import *
from MODEL.Chess_Board import *

class Controller:
    def __init__(self, board, board_view):
        self.board = board
        self.board_view = board_view
        self.selected_piece = None
        self.valid_moves = []

    def handle_events(self, event):
        # Nhấn chuột xuống -> chọn quân
        if event.type == pygame.MOUSEBUTTONDOWN:
            mount_x, mount_y = event.pos
            for p in self.board.pieces:
                if p.rect.collidepoint(mount_x, mount_y):
                    self.selected_piece = p
                    self.selected_piece.offset[0] = p.rect.x - mount_x
                    self.selected_piece.offset[1] = p.rect.y - mount_y
                    self.selected_piece.set_valid_moves(self.board)
                    self.board.update_predict_moves(self.selected_piece)
                    break

        # Kéo chuột -> di chuyển quân theo chuột
        elif event.type == pygame.MOUSEMOTION:
            if self.selected_piece:
                # Tọa độ trỏ chuột được cập nhật liên tục khi giữ chuột kết hợp di chuột
                # => Nên phải cập nhật khung của ảnh liên tục dựa vào trỏ chuột để khung ảnh luôn đi theo chuột
                mount_x, mount_y = event.pos
                self.selected_piece.rect.x = mount_x + self.selected_piece.offset[0]
                self.selected_piece.rect.y = mount_y + self.selected_piece.offset[1]
                # offset cố định cho đến khi chuột được thả

        # Thả chuột -> đặt quân vào ô
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.selected_piece:
                # vị trí quân cờ được được thả
                mount_x, mount_y = event.pos

                # Chuyển tọa độ của chuột về tạo độ x, y là số nguyên chỉ nằm trong (0-7)
                x = mount_x // cell_size
                y = mount_y // cell_size

                # Quân được thả vào ô hợp lệ
                if [x,y] in self.selected_piece.valid_moves:
                    # TH 1: Ăn quân
                    if [x, y] in (self.board.current_coordinates_of_white + self.board.current_coordinates_of_black):
                        deleted_piece = self.board.get_piece_with_coordinates(x,y)
                        self.board.remove_piece(deleted_piece)
                    # TH 2: Ô trống, do ô trống đã nằm trong valid_moves => x,y hợp lệ do đã kiểm tra ở trên

                    # Đặt lại tọa độ cho quân có nước đi hợp lệ
                    self.selected_piece.set_coordinate(x, y)

                # Quân thả vào ô không hợp lệ => quay lại vị trí trước đó
                else:
                    self.selected_piece.set_coordinate(self.selected_piece.current_coordinates[0], self.selected_piece.current_coordinates[1])

                self.board.update_all_coordinates()

                self.selected_piece = None
