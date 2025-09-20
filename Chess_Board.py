import pygame

WHITE = (238, 238, 210)
DARKGREEN = (118, 150, 86)

class Board:
    def __init__(self,row = 8 , column = 8, cell_size = 100):
        self.row = row
        self.column = column
        self.cell_size = cell_size

    def Build_Board(self,screen):
        for r in range(self.row):
            for c in range(self.column):
#                if( i+j % 2 == 0 ) : white cell
#                else green cell
                color = WHITE if (r + c) % 2 == 0 else DARKGREEN
                pygame.draw.rect(screen, color, (r * self.cell_size, c * self.cell_size, self.cell_size, self.cell_size))






