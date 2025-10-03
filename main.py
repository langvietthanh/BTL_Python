import pygame as pg
from pygame._sdl2.controller import Controller
from pygame.locals import *
from MODEL.Chess_Board import *
from MODEL.Piece import *
from CONTROLLER.Controller import *
from VIEW.Board_View import *

pygame.init()

# Create screen
window_height,window_width  = 800,800
img_height,img_width = 60,60
screen = pygame.display.set_mode((window_height,window_width))
pygame.display.set_caption("CHESS_BOARD")

# Create Board
board = Board()

board_view = Board_View(screen,board)
board_view.init_piece()

Controller = Controller(board,board_view)

running = True
while running :
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        else:
            Controller.handle_events(event)
    board_view.draw_board()
pygame.quit()
