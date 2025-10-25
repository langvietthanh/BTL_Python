


class GameState :
    def __init__ (self ,board ):
        """
        Khởi tạo trạng thái game
        
        Args:
            board: Chess_Board object
        """
        self .board =board 
        self .current_turn ='White'
        self .move_history =[]
        self .captured_pieces ={'White':[],'Black':[]}


        self .is_check =False 
        self .is_checkmate =False 
        self .is_stalemate =False 
        self .is_draw =False 
        self .game_over =False 
        self .winner =None 


        self .castling_rights ={
        'White':{'kingside':True ,'queenside':True },
        'Black':{'kingside':True ,'queenside':True }
        }


        self .en_passant_target =None 
        self .en_passant_pawn =None 


        self .halfmove_clock =0 
        self .fullmove_number =1 


        self .position_history =[]

    def switch_turn (self ):
        """Chuyển lượt chơi"""
        self .current_turn ='Black'if self .current_turn =='White'else 'White'
        if self .current_turn =='White':
            self .fullmove_number +=1 

    def add_move_to_history (self ,move ):
        """Thêm nước đi vào lịch sử"""
        self .move_history .append (move )


        if move .is_capture or move .piece .role =='pawn':
            self .halfmove_clock =0 
        else :
            self .halfmove_clock +=1 


        self .position_history .append (self .get_position_hash ())

    def get_position_hash (self ):
        """Tạo hash của vị trí hiện tại để kiểm tra lặp lại"""
        position =[]
        for piece in self .board .pieces :
            position .append ((piece .color ,piece .role ,
            piece .current_coordinates [0 ],
            piece .current_coordinates [1 ]))
        return tuple (sorted (position ))

    def update_castling_rights (self ,move ):
        """Cập nhật quyền nhập thành sau mỗi nước đi"""
        color =move .piece .color 


        if move .piece .role =='king':
            self .castling_rights [color ]['kingside']=False 
            self .castling_rights [color ]['queenside']=False 


        if move .piece .role =='rook':
            if color =='White':
                if move .from_x ==0 and move .from_y ==7 :
                    self .castling_rights [color ]['queenside']=False 
                elif move .from_x ==7 and move .from_y ==7 :
                    self .castling_rights [color ]['kingside']=False 
            else :
                if move .from_x ==0 and move .from_y ==0 :
                    self .castling_rights [color ]['queenside']=False 
                elif move .from_x ==7 and move .from_y ==0 :
                    self .castling_rights [color ]['kingside']=False 


        if move .captured_piece and move .captured_piece .role =='rook':
            captured_color =move .captured_piece .color 
            if captured_color =='White':
                if move .to_x ==0 and move .to_y ==7 :
                    self .castling_rights [captured_color ]['queenside']=False 
                elif move .to_x ==7 and move .to_y ==7 :
                    self .castling_rights [captured_color ]['kingside']=False 
            else :
                if move .to_x ==0 and move .to_y ==0 :
                    self .castling_rights [captured_color ]['queenside']=False 
                elif move .to_x ==7 and move .to_y ==0 :
                    self .castling_rights [captured_color ]['kingside']=False 

    def update_en_passant (self ,move ):
        """Cập nhật trạng thái en passant"""

        self .en_passant_target =None 
        self .en_passant_pawn =None 


        if move .piece .role =='pawn':
            if abs (move .to_y -move .from_y )==2 :

                target_y =(move .from_y +move .to_y )//2 
                self .en_passant_target =[move .to_x ,target_y ]
                self .en_passant_pawn =move .piece 

    def check_for_check (self ,color ):
        """
        Kiểm tra xem vua của màu này có bị chiếu không
        
        Args:
            color: 'White' hoặc 'Black'
        
        Returns:
            bool: True nếu bị chiếu
        """

        king =None 
        for piece in self .board .pieces :
            if piece .role =='king'and piece .color ==color :
                king =piece 
                break 

        if not king :
            return False 

        king_x ,king_y =king .current_coordinates 
        opponent_color ='Black'if color =='White'else 'White'


        for piece in self .board .pieces :
            if piece .color ==opponent_color :

                if self ._can_piece_attack (piece ,king_x ,king_y ):
                    return True 

        return False 

    def _can_piece_attack (self ,piece ,target_x ,target_y ):
        """Kiểm tra quân có thể tấn công ô target không"""
        x ,y =piece .current_coordinates 
        dx =target_x -x 
        dy =target_y -y 

        if piece .role =='pawn':

            direction =1 if piece .color =='Black'else -1 
            if dy ==direction and abs (dx )==1 :
                return True 

        elif piece .role =='knight':

            if (abs (dx )==2 and abs (dy )==1 )or (abs (dx )==1 and abs (dy )==2 ):
                return True 

        elif piece .role =='bishop':

            if abs (dx )==abs (dy )and dx !=0 :
                return self ._is_path_clear (x ,y ,target_x ,target_y )

        elif piece .role =='rook':

            if (dx ==0 or dy ==0 )and (dx !=0 or dy !=0 ):
                return self ._is_path_clear (x ,y ,target_x ,target_y )

        elif piece .role =='queen':

            if (dx ==0 or dy ==0 or abs (dx )==abs (dy ))and (dx !=0 or dy !=0 ):
                return self ._is_path_clear (x ,y ,target_x ,target_y )

        elif piece .role =='king':

            if abs (dx )<=1 and abs (dy )<=1 and (dx !=0 or dy !=0 ):
                return True 

        return False 

    def _is_path_clear (self ,from_x ,from_y ,to_x ,to_y ):
        """Kiểm tra đường đi có trống không (cho xe, tượng, hậu)"""
        dx =0 if to_x ==from_x else (1 if to_x >from_x else -1 )
        dy =0 if to_y ==from_y else (1 if to_y >from_y else -1 )

        x ,y =from_x +dx ,from_y +dy 
        while x !=to_x or y !=to_y :
            if not self .board .cell_is_empty (x ,y ):
                return False 
            x +=dx 
            y +=dy 

        return True 

    def check_for_checkmate (self ,color ):
        """
        Kiểm tra chiếu hết
        
        Args:
            color: Màu đang bị check
        
        Returns:
            bool: True nếu bị chiếu hết
        """

        if not self .check_for_check (color ):
            return False 




        from ENGINE .Move_Generator import MoveGenerator 
        move_gen =MoveGenerator (self .board )
        legal_moves =move_gen .generate_all_legal_moves (color ,self )

        return len (legal_moves )==0 

    def check_for_stalemate (self ,color ):
        """
        Kiểm tra hòa cờ (stalemate): không bị chiếu nhưng không có nước đi hợp lệ
        
        Args:
            color: Màu đang xét
        
        Returns:
            bool: True nếu stalemate
        """

        if self .check_for_check (color ):
            return False 


        from ENGINE .Move_Generator import MoveGenerator 
        move_gen =MoveGenerator (self .board )
        legal_moves =move_gen .generate_all_legal_moves (color ,self )

        return len (legal_moves )==0 

    def check_for_draw (self ):
        """
        Kiểm tra các trường hợp hòa cờ
        
        Returns:
            bool: True nếu hòa
        """

        if self .halfmove_clock >=100 :
            return True 


        current_position =self .get_position_hash ()
        if self .position_history .count (current_position )>=3 :
            return True 


        if self .is_insufficient_material ():
            return True 

        return False 

    def is_insufficient_material (self ):
        """
        Kiểm tra xem có đủ quân để chiếu hết không
        Hòa nếu chỉ còn:
        - Vua vs Vua
        - Vua + Mã vs Vua
        - Vua + Tượng vs Vua
        """
        pieces =self .board .pieces 


        if len (pieces )==2 :
            return True 


        if len (pieces )==3 :
            for piece in pieces :
                if piece .role in ['knight','bishop']:
                    return True 


        if len (pieces )==4 :
            bishops =[p for p in pieces if p .role =='bishop']
            if len (bishops )==2 :
                x1 ,y1 =bishops [0 ].current_coordinates 
                x2 ,y2 =bishops [1 ].current_coordinates 
                if (x1 +y1 )%2 ==(x2 +y2 )%2 :
                    return True 

        return False 

    def update_game_state (self ):
        """Cập nhật toàn bộ trạng thái game sau mỗi nước đi"""

        side_to_move =self .current_turn 
        opponent_color ='Black'if side_to_move =='White'else 'White'


        self .is_check =self .check_for_check (side_to_move )


        self .is_checkmate =self .check_for_checkmate (side_to_move )


        if not self .is_checkmate :
            self .is_stalemate =self .check_for_stalemate (side_to_move )
            self .is_draw =self .check_for_draw ()


        if self .is_checkmate :
            self .game_over =True 
            self .winner =opponent_color 
        elif self .is_stalemate or self .is_draw :
            self .game_over =True 
            self .winner =None 

    def get_game_status (self ):
        """Lấy trạng thái game dạng string"""
        if self .is_checkmate :
            return f"Checkmate! {self .winner } wins!"
        elif self .is_stalemate :
            return "Stalemate!"
        elif self .is_draw :
            return "Draw!"
        elif self .is_check :
            opponent ='Black'if self .current_turn =='White'else 'White'
            return f"{opponent } is in check!"
        else :
            return f"{self .current_turn }'s turn"

    def reset (self ):
        """Reset trạng thái game"""
        self .current_turn ='White'
        self .move_history =[]
        self .captured_pieces ={'White':[],'Black':[]}
        self .is_check =False 
        self .is_checkmate =False 
        self .is_stalemate =False 
        self .is_draw =False 
        self .game_over =False 
        self .winner =None 
        self .castling_rights ={
        'White':{'kingside':True ,'queenside':True },
        'Black':{'kingside':True ,'queenside':True }
        }
        self .en_passant_target =None 
        self .en_passant_pawn =None 
        self .halfmove_clock =0 
        self .fullmove_number =1 
        self .position_history =[]