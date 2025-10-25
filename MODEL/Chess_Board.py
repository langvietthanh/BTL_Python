
import pygame as pg 
from MODEL .Piece import *

class Board :
    def __init__ (self ):
        self .pieces =[]
        self .current_coordinates_of_black =[]
        self .current_coordinates_of_white =[]
        self .predict_moves =[]

    def get_piece_with_coordinates (self ,x ,y ):
        for piece in self .pieces :
            if piece .current_coordinates ==[x ,y ]:
                return piece 
        return None 

    def add_piece (self ,piece ):
        self .pieces .append (piece )
        self .update_all_coordinates ()

    def remove_piece (self ,piece ):
        self .pieces .remove (piece )
        self .update_all_coordinates ()

    def update_all_coordinates (self ):
        self .current_coordinates_of_black =[]
        self .current_coordinates_of_white =[]
        for piece in self .pieces :
            if piece .color =='Black':
                self .current_coordinates_of_black .append (piece .current_coordinates )
            else :
                self .current_coordinates_of_white .append (piece .current_coordinates )

    def update_predict_moves (self ,selected_piece ):
        if selected_piece .role =='king':
            self .predict_moves =[]
            for piece in self .pieces :
                if selected_piece .color !=piece .color :
                    if piece .role !='pawn':
                        piece .set_valid_moves (self )
                        self .predict_moves +=piece .valid_moves 

                    else :
                        predict_move =[]
                        piece .set_pawn_moves_case_king (self ,predict_move )
                        self .predict_moves +=predict_move 

    def cell_have_white_piece (self ,x ,y ):
        return [x ,y ]in self .current_coordinates_of_white 

    def cell_have_black_piece (self ,x ,y ):
        return [x ,y ]in self .current_coordinates_of_black 

    def cell_is_empty (self ,x ,y ):
        return ([x ,y ]not in self .current_coordinates_of_white )and ([x ,y ]not in self .current_coordinates_of_black )
