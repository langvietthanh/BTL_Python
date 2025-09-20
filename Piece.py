import pygame
cell_size=100

class Piece:
    # img đã được load trước đó bằng pygame ở file main
    # role = pawn, bishop, knight, rook, queen, king
    # self là một quan co
    def __init__(self,img,color,role,x,y,screen):
        self.color = color
        self.role = role
        self.img = pygame.transform.scale(img,(80,80))
        self.x = x
        self.y = y
        self.img_rect = img.get_rect(topleft = (x * cell_size+10,y * cell_size+10))
        self.screen = screen
        self.screen.blit(self.img, self.img_rect)

    # đặt lại tọa độ
    def set_coordinate(self,x,y):
        self.x = x
        self.y = y
        self.img_rect = self.img.get_rect(topleft = (x * cell_size+10,y * cell_size+10))
        self.screen.blit (self.img, self.img_rect)

    # def show_piece(self,screen):
    #     screen.blit(self.img,self.img_rect)


