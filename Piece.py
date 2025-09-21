import pygame
cell_size=100

class Piece:
    # img đã được load trước đó bằng pygame ở file main
    # role = pawn, bishop, knight, rook, queen, king
    # self là một quan co
    def __init__(self,img,color,role,x,y,screen):
        self.color = color
        self.role = role
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(img,(80,80))
        self.rect = self.img.get_rect()
        self.set_coordinate(self.x,self.y)

    # đặt lại tọa độ
    def set_coordinate(self,x,y):
        self.x = x * cell_size + 10
        self.y = y * cell_size + 10
        self.rect.topleft = (self.x, self.y)

    def show_piece(self,screen):
        screen.blit(self.img,self.rect)



