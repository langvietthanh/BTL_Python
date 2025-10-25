
import pygame

CELL_SIZE =100 

class Piece :
    def __init__ (self ,img ,color ,role ,x ,y ):
        """
        Khởi tạo quân cờ
        
        Args:
            img: Pygame image
            color: 'White' hoặc 'Black'
            role: 'pawn', 'bishop', 'knight', 'rook', 'queen', 'king'
            x, y: Tọa độ ban đầu (0-7)
        """
        self .color =color 
        self .role =role 
        self .offset =[0 ,0 ]
        self .current_coordinates =[x ,y ]
        self .before_coordinates =[x ,y ]
        self .img =pygame .transform .scale (img ,(100 ,100 ))
        self .rect =self .img .get_rect (
        topleft =(self .current_coordinates [0 ]*CELL_SIZE ,
        self .current_coordinates [1 ]*CELL_SIZE )
        )
        self .valid_moves =[]
        self .replaced_by =[]

    def set_coordinate (self ,x ,y ):
        """
        Đặt lại tọa độ cho quân
        
        Args:
            x, y: Tọa độ mới
        """

        if [x ,y ]!=self .current_coordinates :
            self .before_coordinates =self .current_coordinates 
            self .current_coordinates =[x ,y ]
        self .set_rect ()

    def set_rect (self ):
        """Cập nhật rect của pygame"""
        self .rect .x =self .current_coordinates [0 ]*CELL_SIZE 
        self .rect .y =self .current_coordinates [1 ]*CELL_SIZE 

    def had_move (self ):
        """
        Kiểm tra quân đã di chuyển chưa
        
        Returns:
            bool: True nếu đã di chuyển
        """
        return self .current_coordinates !=self .before_coordinates 

    def set_valid_moves (self ,board ):
        """
        Tính toán valid moves (legacy - để tương thích với code cũ)
        Nên dùng Move_Generator thay thế
        """
        self .valid_moves =[]

        if self .role =='pawn':
            self ._set_pawn_moves_legacy (board )
        elif self .role =='rook':
            self ._set_rook_moves_legacy (board )
        elif self .role =='knight':
            self ._set_knight_moves_legacy (board )
        elif self .role =='bishop':
            self ._set_bishop_moves_legacy (board )
        elif self .role =='queen':
            self ._set_queen_moves_legacy (board )
        elif self .role =='king':
            self ._set_king_moves_legacy (board )

    def _set_pawn_moves_legacy (self ,board ):
        """Legacy pawn moves"""
        pawn_steps =[[0 ,1 ],[1 ,1 ],[-1 ,1 ]]
        if self .current_coordinates ==self .before_coordinates :
            pawn_steps .append ([0 ,2 ])

        for step in pawn_steps :
            if self .color =='Black':
                next_move =[step [0 ]+self .current_coordinates [0 ],
                step [1 ]+self .current_coordinates [1 ]]
            else :
                next_move =[-step [0 ]+self .current_coordinates [0 ],
                -step [1 ]+self .current_coordinates [1 ]]

            if 0 <=next_move [0 ]<=7 and 0 <=next_move [1 ]<=7 :
                if next_move [0 ]!=self .current_coordinates [0 ]:

                    if self .color =='Black':
                        if board .cell_have_white_piece (next_move [0 ],next_move [1 ]):
                            self .valid_moves .append (next_move )
                    else :
                        if board .cell_have_black_piece (next_move [0 ],next_move [1 ]):
                            self .valid_moves .append (next_move )
                elif board .cell_is_empty (next_move [0 ],next_move [1 ]):
                    self .valid_moves .append (next_move )

    def _set_rook_moves_legacy (self ,board ):
        """Legacy rook moves"""
        rook_steps =[[1 ,0 ],[-1 ,0 ],[0 ,1 ],[0 ,-1 ]]
        for step in rook_steps :
            x ,y =self .current_coordinates [0 ]+step [0 ],self .current_coordinates [1 ]+step [1 ]
            while 0 <=x <=7 and 0 <=y <=7 :
                if self .color =='White':
                    if board .cell_have_black_piece (x ,y ):
                        self .valid_moves .append ([x ,y ])
                        break 
                    elif board .cell_have_white_piece (x ,y ):
                        break 
                else :
                    if board .cell_have_white_piece (x ,y ):
                        self .valid_moves .append ([x ,y ])
                        break 
                    elif board .cell_have_black_piece (x ,y ):
                        break 

                if board .cell_is_empty (x ,y ):
                    self .valid_moves .append ([x ,y ])

                x ,y =x +step [0 ],y +step [1 ]

    def _set_knight_moves_legacy (self ,board ):
        """Legacy knight moves"""
        knight_steps =[[1 ,2 ],[1 ,-2 ],[2 ,1 ],[2 ,-1 ],
        [-1 ,2 ],[-1 ,-2 ],[-2 ,1 ],[-2 ,-1 ]]
        for step in knight_steps :
            next_move =[step [0 ]+self .current_coordinates [0 ],
            step [1 ]+self .current_coordinates [1 ]]

            if 0 <=next_move [0 ]<=7 and 0 <=next_move [1 ]<=7 :
                if self .color =='Black':
                    if board .cell_have_white_piece (next_move [0 ],next_move [1 ]):
                        self .valid_moves .append (next_move )
                else :
                    if board .cell_have_black_piece (next_move [0 ],next_move [1 ]):
                        self .valid_moves .append (next_move )

                if board .cell_is_empty (next_move [0 ],next_move [1 ]):
                    self .valid_moves .append (next_move )

    def _set_bishop_moves_legacy (self ,board ):
        """Legacy bishop moves"""
        bishop_steps =[[1 ,1 ],[-1 ,-1 ],[-1 ,1 ],[1 ,-1 ]]
        for step in bishop_steps :
            x ,y =self .current_coordinates [0 ]+step [0 ],self .current_coordinates [1 ]+step [1 ]

            while 0 <=x <=7 and 0 <=y <=7 :
                if self .color =='White':
                    if board .cell_have_black_piece (x ,y ):
                        self .valid_moves .append ([x ,y ])
                        break 
                    elif board .cell_have_white_piece (x ,y ):
                        break 
                else :
                    if board .cell_have_white_piece (x ,y ):
                        self .valid_moves .append ([x ,y ])
                        break 
                    elif board .cell_have_black_piece (x ,y ):
                        break 

                if board .cell_is_empty (x ,y ):
                    self .valid_moves .append ([x ,y ])

                x ,y =x +step [0 ],y +step [1 ]

    def _set_queen_moves_legacy (self ,board ):
        """Legacy queen moves"""
        self ._set_bishop_moves_legacy (board )
        self ._set_rook_moves_legacy (board )

    def _set_king_moves_legacy (self ,board ):
        """Legacy king moves"""
        king_valid_steps =[[x ,y ]for x in range (-1 ,2 )for y in range (-1 ,2 )
        if (x !=0 or y !=0 )]

        for step in king_valid_steps :
            next_move =[step [0 ]+self .current_coordinates [0 ],
            step [1 ]+self .current_coordinates [1 ]]
            if 0 <=next_move [0 ]<=7 and 0 <=next_move [1 ]<=7 :
                piece =board .get_piece_with_coordinates (next_move [0 ],next_move [1 ])

                if piece is None :
                    self .valid_moves .append (next_move )
                elif self .color =='Black':
                    if board .cell_have_white_piece (next_move [0 ],next_move [1 ]):
                        self .valid_moves .append (next_move )
                else :
                    if board .cell_have_black_piece (next_move [0 ],next_move [1 ]):
                        self .valid_moves .append (next_move )

    def __deepcopy__ (self ,memo ):
        """Tạo bản sao sâu chỉ chứa trạng thái logic, bỏ qua surface img.

        Bản sao này đủ dùng cho tính toán luật (không dùng để vẽ).
        """
        cls =self .__class__ 
        copy_obj =cls .__new__ (cls )
        memo [id (self )]=copy_obj 


        copy_obj .color =self .color 
        copy_obj .role =self .role 
        copy_obj .offset =list (self .offset )
        copy_obj .current_coordinates =list (self .current_coordinates )
        copy_obj .before_coordinates =list (self .before_coordinates )


        copy_obj .img =None 
        copy_obj .rect =pygame .Rect (
        copy_obj .current_coordinates [0 ]*CELL_SIZE ,
        copy_obj .current_coordinates [1 ]*CELL_SIZE ,
        CELL_SIZE ,
        CELL_SIZE ,
        )


        copy_obj .valid_moves =[list (m )for m in self .valid_moves ]
        copy_obj .replaced_by =list (self .replaced_by )

        return copy_obj 
