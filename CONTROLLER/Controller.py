import pygame as pg
from MODEL.Piece import *
from MODEL.Chess_Board import *

class Controller:
    def __init__(self, board, board_view):
        self.board = board
        self.board_view = board_view
        self.selected_piece = None

    def handle_events(self, event):
        # Nhấn chuột xuống -> chọn quân
        if event.type == pygame.MOUSEBUTTONDOWN:
            mount_x, mount_y = event.pos
            for p in self.board.pieces:
                if p.rect.collidepoint(mount_x, mount_y):
                    self.selected_piece = p
                    self.selected_piece.offset[0] = p.rect.x - mount_x
                    self.selected_piece.offset[1] = p.rect.y - mount_y
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
                mount_x, mount_y = event.pos  # quân cờ đã được thả
                # Chuyển tọa độ của chuột về tạo độ x, y là số nguyên chỉ nằm trong (0-7)
                x = mount_x // cell_size
                y = mount_y // cell_size
                if (0 <= x < 8 and 0 <= y < 8):
                    # Ô trong bàn cờ
                    self.selected_piece.set_coordinate(x, y)
                else:
                    self.selected_piece.set_coordinate(self.selected_piece.current_coordinates[0], self.selected_piece.current_coordinates[1])
                self.selected_piece = None
