


class Move :
    def __init__ (self ,piece ,from_x ,from_y ,to_x ,to_y ):
        """
        Khởi tạo nước đi
        
        Args:
            piece: Quân cờ thực hiện nước đi
            from_x, from_y: Vị trí xuất phát
            to_x, to_y: Vị trí đích
        """
        self .piece =piece 
        self .from_x =from_x 
        self .from_y =from_y 
        self .to_x =to_x 
        self .to_y =to_y 


        self .captured_piece =None 
        self .is_capture =False 
        self .is_castling =False 
        self .is_en_passant =False 
        self .promotion_piece =None 


        self .is_check =False 
        self .is_checkmate =False 


        self .previous_state =None 

    def __eq__ (self ,other ):
        """
        So sánh hai nước đi có giống nhau không
        """
        if not isinstance (other ,Move ):
            return False 
        return (self .from_x ==other .from_x and 
        self .from_y ==other .from_y and 
        self .to_x ==other .to_x and 
        self .to_y ==other .to_y )

    def __repr__ (self ):
        """
        Hiển thị nước đi dạng string
        """
        from_pos =f"({self .from_x },{self .from_y })"
        to_pos =f"({self .to_x },{self .to_y })"
        piece_name =f"{self .piece .color } {self .piece .role }"

        result =f"{piece_name }: {from_pos } -> {to_pos }"

        if self .is_capture :
            result +=f" [captures {self .captured_piece .role }]"
        if self .is_castling :
            result +=" [castling]"
        if self .is_en_passant :
            result +=" [en passant]"
        if self .promotion_piece :
            result +=f" [promotes to {self .promotion_piece }]"
        if self .is_checkmate :
            result +=" [CHECKMATE]"
        elif self .is_check :
            result +=" [CHECK]"

        return result 

    def to_dict (self ):
        """
        Chuyển đổi sang dictionary để lưu trữ
        """
        return {
        'from':[self .from_x ,self .from_y ],
        'to':[self .to_x ,self .to_y ],
        'piece':self .piece .role ,
        'color':self .piece .color ,
        'is_capture':self .is_capture ,
        'is_castling':self .is_castling ,
        'is_en_passant':self .is_en_passant ,
        'promotion':self .promotion_piece ,
        'is_check':self .is_check ,
        'is_checkmate':self .is_checkmate 
        }

    def copy (self ):
        """
        Tạo bản sao của nước đi
        """
        new_move =Move (self .piece ,self .from_x ,self .from_y ,self .to_x ,self .to_y )
        new_move .captured_piece =self .captured_piece 
        new_move .is_capture =self .is_capture 
        new_move .is_castling =self .is_castling 
        new_move .is_en_passant =self .is_en_passant 
        new_move .promotion_piece =self .promotion_piece 
        new_move .is_check =self .is_check 
        new_move .is_checkmate =self .is_checkmate 
        return new_move 