import pygame as pg
from MODEL .Piece import *
from UTILS .Constants import *

class Board_View :
    def __init__ (self ,screen ,board ):
        self .screen =screen 
        self .board =board 
        self .selected_piece =None 
        self .valid_moves =[]
        self .last_move =None 
        self .board_rotated =False 

    def init_piece (self ):
        """Khởi tạo tất cả quân cờ"""


        img_black_rook =pg .image .load ("PNG/black_rook.png")
        piece_black_LeftRook =Piece (img_black_rook ,"Black","rook",0 ,0 )
        piece_black_RightRook =Piece (img_black_rook ,"Black","rook",7 ,0 )


        img_black_knight =pg .image .load ("PNG/black_knight.png")
        piece_black_LeftKnight =Piece (img_black_knight ,"Black","knight",1 ,0 )
        piece_black_RightKnight =Piece (img_black_knight ,"Black","knight",6 ,0 )


        img_black_bishop =pg .image .load ("PNG/black_bishop.png")
        piece_black_LeftBishop =Piece (img_black_bishop ,"Black","bishop",2 ,0 )
        piece_black_RightBishop =Piece (img_black_bishop ,"Black","bishop",5 ,0 )


        img_black_queen =pg .image .load ("PNG/black_queen.png")
        piece_black_Queen =Piece (img_black_queen ,"Black","queen",3 ,0 )


        img_black_king =pg .image .load ("PNG/black_king.png")
        piece_black_King =Piece (img_black_king ,"Black","king",4 ,0 )


        piece_black_pawn =[]
        img_black_pawn =pg .image .load ("PNG/black_pawn.png")
        for x_i in range (8 ):
            pawn =Piece (img_black_pawn ,"Black","pawn",x_i ,1 )
            piece_black_pawn .append (pawn )



        img_white_rook =pg .image .load ("PNG/white_rook.png")
        piece_white_LeftRook =Piece (img_white_rook ,"White","rook",0 ,7 )
        piece_white_RightRook =Piece (img_white_rook ,"White","rook",7 ,7 )


        img_white_knight =pg .image .load ("PNG/white_knight.png")
        piece_white_LeftKnight =Piece (img_white_knight ,"White","knight",1 ,7 )
        piece_white_RightKnight =Piece (img_white_knight ,"White","knight",6 ,7 )


        img_white_bishop =pg .image .load ("PNG/white_bishop.png")
        piece_white_LeftBishop =Piece (img_white_bishop ,"White","bishop",2 ,7 )
        piece_white_RightBishop =Piece (img_white_bishop ,"White","bishop",5 ,7 )


        img_white_queen =pg .image .load ("PNG/white_queen.png")
        piece_white_Queen =Piece (img_white_queen ,"White","queen",3 ,7 )


        img_white_king =pg .image .load ("PNG/white_king.png")
        piece_white_King =Piece (img_white_king ,"White","king",4 ,7 )


        piece_white_pawn =[]
        img_white_pawn =pg .image .load ("PNG/white_pawn.png")
        for x_i in range (8 ):
            pawn =Piece (img_white_pawn ,"White","pawn",x_i ,6 )
            piece_white_pawn .append (pawn )



        self .board .add_piece (piece_black_LeftRook )
        self .board .add_piece (piece_black_LeftKnight )
        self .board .add_piece (piece_black_LeftBishop )
        self .board .add_piece (piece_black_Queen )
        self .board .add_piece (piece_black_King )
        self .board .add_piece (piece_black_RightRook )
        self .board .add_piece (piece_black_RightKnight )
        self .board .add_piece (piece_black_RightBishop )
        for pawn in piece_black_pawn :
            self .board .add_piece (pawn )


        self .board .add_piece (piece_white_LeftRook )
        self .board .add_piece (piece_white_LeftKnight )
        self .board .add_piece (piece_white_LeftBishop )
        self .board .add_piece (piece_white_Queen )
        self .board .add_piece (piece_white_King )
        self .board .add_piece (piece_white_RightRook )
        self .board .add_piece (piece_white_RightKnight )
        self .board .add_piece (piece_white_RightBishop )
        for pawn in piece_white_pawn :
            self .board .add_piece (pawn )

    def draw_board (self ):
        """Vẽ bàn cờ chính"""
        if self .selected_piece or self .valid_moves :
            self .draw_current_board ()
        else :
            self .draw_blank_board ()

    def draw_blank_board (self ):
        """Vẽ bàn cờ trống (không highlight)"""
        for r in range (8 ):
            for c in range (8 ):

                display_r ,display_c =self .get_display_coordinates (r ,c )
                color =WHITE_CELL if (r +c )%2 ==0 else DARK_CELL 
                pg .draw .rect (self .screen ,color ,
                (display_r *CELL_SIZE ,display_c *CELL_SIZE ,CELL_SIZE ,CELL_SIZE ))


        if self .last_move :
            self .highlight_last_move ()

        self .draw_pieces ()

    def draw_current_board (self ):
        """Vẽ bàn cờ với highlight"""
        for r in range (8 ):
            for c in range (8 ):

                display_r ,display_c =self .get_display_coordinates (r ,c )

                color =WHITE_CELL if (r +c )%2 ==0 else DARK_CELL 
                pg .draw .rect (self .screen ,color ,
                (display_r *CELL_SIZE ,display_c *CELL_SIZE ,CELL_SIZE ,CELL_SIZE ))


                if (self .selected_piece and 
                self .selected_piece .current_coordinates ==[r ,c ]):
                    self .draw_highlight (display_r ,display_c ,HIGHLIGHT_SELECTED )


                if self .valid_moves :
                    for move in self .valid_moves :
                        if move .to_x ==r and move .to_y ==c :
                            if move .is_capture :
                                self .draw_highlight (display_r ,display_c ,HIGHLIGHT_CAPTURE )
                            else :
                                self .draw_empty_cell_highlight (display_r ,display_c )


        if self .last_move :
            self .highlight_last_move ()

        self .draw_pieces ()

    def draw_pieces (self ):
        """Vẽ tất cả quân cờ"""
        for p in self .board .pieces :

            display_x ,display_y =self .get_display_coordinates (p .current_coordinates [0 ],p .current_coordinates [1 ])

            display_rect =p .img .get_rect (
            topleft =(display_x *CELL_SIZE ,display_y *CELL_SIZE )
            )
            self .screen .blit (p .img ,display_rect )

    def draw_highlight (self ,r ,c ,color ):
        """Vẽ highlight cho ô"""
        surface =pg .Surface ((CELL_SIZE ,CELL_SIZE ),pg .SRCALPHA )
        surface .fill (color )
        self .screen .blit (surface ,(r *CELL_SIZE ,c *CELL_SIZE ))

    def draw_empty_cell_highlight (self ,r ,c ):
        """Vẽ dot nhỏ cho ô trống có thể đi"""
        center_x =r *CELL_SIZE +CELL_SIZE //2 
        center_y =c *CELL_SIZE +CELL_SIZE //2 
        pg .draw .circle (self .screen ,HIGHLIGHT_MOVE ,(center_x ,center_y ),15 )

    def draw_king_check (self ,r ,c ):
        """Vẽ highlight cho vua bị chiếu"""
        pg .draw .rect (self .screen ,HIGHLIGHT_CHECK ,
        (r *CELL_SIZE ,c *CELL_SIZE ,CELL_SIZE ,CELL_SIZE ))

    def highlight_last_move (self ):
        """Highlight nước đi cuối cùng"""
        if not self .last_move :
            return 


        from_display_x ,from_display_y =self .get_display_coordinates (self .last_move .from_x ,self .last_move .from_y )
        to_display_x ,to_display_y =self .get_display_coordinates (self .last_move .to_x ,self .last_move .to_y )


        self .draw_highlight (from_display_x ,from_display_y ,HIGHLIGHT_LAST_MOVE )


        self .draw_highlight (to_display_x ,to_display_y ,HIGHLIGHT_LAST_MOVE )

    def set_valid_moves (self ,moves ):
        """Đặt danh sách nước đi hợp lệ để highlight"""
        self .valid_moves =moves 

    def set_last_move (self ,move ):
        """Đặt nước đi cuối cùng"""
        self .last_move =move 

    def toggle_board_rotation (self ):
        """Xoay bàn cờ"""
        self .board_rotated =not self .board_rotated 

    def get_display_coordinates (self ,x ,y ):
        """
        Chuyển đổi tọa độ logic sang tọa độ hiển thị
        Nếu board bị xoay, đảo ngược tọa độ
        """
        if self .board_rotated :
            return (7 -x ,7 -y )
        return (x ,y )

    def get_logic_coordinates (self ,x ,y ):
        """
        Chuyển đổi tọa độ hiển thị sang tọa độ logic
        Nếu board bị xoay, đảo ngược tọa độ
        """
        if self .board_rotated :
            return (7 -x ,7 -y )
        return (x ,y )

