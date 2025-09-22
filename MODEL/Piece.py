import pygame
cell_size=100

# role = pawn, bishop, knight, rook, queen, king
# offset : khoảng cách tọa độ chuột với góc trên trái
# current_coordinates : Tọa độ hiện tại của quân cờ
# before_coordinates : Tọa độ trước đó của quân cờ

class Piece:
    def __init__(self,img,color,role,x,y):
        self.color = color
        self.role = role
        self.offset = [0,0]
        self.current_coordinates = [x,y]
        self.before_coordinates = [x,y]
        self.img = pygame.transform.scale(img,(100,100))
        self.rect = self.img.get_rect(topleft = (self.current_coordinates[0] * cell_size ,
                                                 self.current_coordinates[1] * cell_size))

    # đặt lại tọa độ
    def set_coordinate(self,x,y):
        self.before_coordinates = self.current_coordinates
        self.current_coordinates = [x,y]
        self.set_rect()

    def set_rect(self):
        self.rect.x = self.current_coordinates[0] * cell_size
        self.rect.y = self.current_coordinates[1] * cell_size



