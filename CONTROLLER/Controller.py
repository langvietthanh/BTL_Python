
import pygame as pg 
from MODEL .Piece import *
from MODEL .Chess_Board import *

class Controller :
    def __init__ (self ,board ,board_view ):
        self .board =board 
        self .board_view =board_view 
        self .selected_piece =None 
        self .valid_moves =[]

    def handle_events (self ,event ):
        """
        Xử lý events cơ bản (giữ để tương thích)
        Nên dùng Game_Controller thay thế
        """

        if event .type ==pg .MOUSEBUTTONDOWN :
            mount_x ,mount_y =event .pos 
            for p in self .board .pieces :
                if p .rect .collidepoint (mount_x ,mount_y ):
                    self .selected_piece =self .board_view .selected_piece =p 

                    self .selected_piece .offset [0 ]=p .rect .x -mount_x 
                    self .selected_piece .offset [1 ]=p .rect .y -mount_y 

                    self .board .update_all_coordinates ()
                    self .board .update_predict_moves (self .selected_piece )
                    self .selected_piece .set_valid_moves (self .board )
                    break 


        elif event .type ==pg .MOUSEMOTION :
            if self .selected_piece :
                mount_x ,mount_y =event .pos 
                self .selected_piece .rect .x =mount_x +self .selected_piece .offset [0 ]
                self .selected_piece .rect .y =mount_y +self .selected_piece .offset [1 ]


        elif event .type ==pg .MOUSEBUTTONUP :
            if self .selected_piece :
                mount_x ,mount_y =event .pos 


                from UTILS .Constants import CELL_SIZE 
                x =mount_x //CELL_SIZE 
                y =mount_y //CELL_SIZE 


                if [x ,y ]in self .selected_piece .valid_moves :

                    if [x ,y ]in (self .board .current_coordinates_of_white +self .board .current_coordinates_of_black ):
                        deleted_piece =self .board .get_piece_with_coordinates (x ,y )
                        self .board .remove_piece (deleted_piece )


                    self .selected_piece .set_coordinate (x ,y )


                else :
                    self .selected_piece .set_coordinate (
                    self .selected_piece .current_coordinates [0 ],
                    self .selected_piece .current_coordinates [1 ]
                    )

                self .board_view .selected_piece =None 
                self .selected_piece =None 
