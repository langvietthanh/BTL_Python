import pygame as pg
import sys, os
from pygame.locals import *
from Chess_Board import *
from Piece import *

pygame.init()
running = True
window_height,window_width  = 800,800
img_height,img_width = 60,60

screen = pygame.display.set_mode((window_height,window_width))
pygame.display.set_caption("CHESS_BOARD")

# Board
board = Board()
board.init_piece()

def replace_piece(piece):
    for p in board.pieces:
        if p.rect.colliderect(x * cell_size + 10, y * cell_size + 10):
            if p.color != piece.color:
                board.remove_piece(p)
                piece.set_coordinate(x,y)
            else:
                break

Pieces = board.pieces
selected_piece = None
offset_x = 0
offset_y = 0

while running :
    board.build_board(screen)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # Nhấn chuột xuống -> chọn quân
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mount_x, mount_y = event.pos
            for p in board.pieces:
                if p.rect.collidepoint(mount_x, mount_y):
                    selected_piece = p
                    # offset_x(y) lưu khoảng cách góc trên trái với vị trí click chuột
                    offset_x = p.rect.x - mount_x
                    offset_y = p.rect.y - mount_y
                    break

        # Kéo chuột -> di chuyển quân theo chuột
        elif event.type == pygame.MOUSEMOTION:
            if selected_piece:
                mount_x, mount_y = event.pos
                # Tọa độ trỏ chuột được cập nhật liên tục khi giữ chuột kết hợp di chuột
                # Nên phải cập nhật khung của ảnh liên tục dựa vào trỏ chuột để khung ảnh luôn đi theo chuột
                selected_piece.rect.x = mount_x + offset_x
                selected_piece.rect.y = mount_y + offset_y
                # offset_x(y) cố định cho đến khi chuột được thả

        # Thả chuột -> đặt quân vào ô
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_piece:
                mount_x, mount_y = event.pos
                # Chuyển tọa độ của chuột về tạo độ x, y là số nguyên chỉ nằm trong (0-7)
                x = (mount_x - 10) // cell_size
                y = (mount_y - 10) // cell_size
                selected_piece.set_coordinate(x, y)
                selected_piece = None
    pygame.display.update()
pygame.quit()
