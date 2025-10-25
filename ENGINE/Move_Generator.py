

from MODEL .Move import Move 
from UTILS .Helper import is_valid_position 
import copy 

def copy_board (board ):
    """Tạo bản sao sâu của board"""
    return copy .deepcopy (board )

class MoveGenerator :
    def __init__ (self ,board ):
        """
        Khởi tạo move generator
        
        Args:
            board: Chess_Board object
        """
        self .board =board 

    def generate_all_moves (self ,color ,game_state =None ):
        """
        Sinh tất cả pseudo-legal moves (chưa kiểm tra check)
        
        Args:
            color: 'White' hoặc 'Black'
            game_state: GameState object (optional, for en passant)
        
        Returns:
            List[Move]: Danh sách các nước đi
        """
        moves =[]
        for piece in self .board .pieces :
            if piece .color ==color :
                piece_moves =self .generate_pseudo_legal_moves (piece ,game_state )
                moves .extend (piece_moves )
        return moves 

    def generate_pseudo_legal_moves (self ,piece ,game_state =None ):
        """
        Sinh các nước đi pseudo-legal cho một quân (chưa check vua bị chiếu)
        """
        if piece .role =='pawn':
            return self .generate_pawn_moves (piece ,game_state )
        elif piece .role =='knight':
            return self .generate_knight_moves (piece )
        elif piece .role =='bishop':
            return self .generate_bishop_moves (piece )
        elif piece .role =='rook':
            return self .generate_rook_moves (piece )
        elif piece .role =='queen':
            return self .generate_queen_moves (piece )
        elif piece .role =='king':
            return self .generate_king_moves (piece )
        return []

    def generate_pawn_moves (self ,pawn ,game_state =None ):
        """Sinh nước đi cho tốt"""
        moves =[]
        x ,y =pawn .current_coordinates 
        direction =1 if pawn .color =='Black'else -1 


        new_y =y +direction 
        if is_valid_position (x ,new_y )and self .board .cell_is_empty (x ,new_y ):
            move =Move (pawn ,x ,y ,x ,new_y )

            if (pawn .color =='White'and new_y ==0 )or (pawn .color =='Black'and new_y ==7 ):
                move .promotion_piece ='queen'
            moves .append (move )


            if pawn .current_coordinates ==pawn .before_coordinates :
                new_y2 =y +2 *direction 
                if is_valid_position (x ,new_y2 )and self .board .cell_is_empty (x ,new_y2 ):
                    moves .append (Move (pawn ,x ,y ,x ,new_y2 ))


        for dx in [-1 ,1 ]:
            new_x =x +dx 
            new_y =y +direction 
            if is_valid_position (new_x ,new_y ):

                if pawn .color =='White'and self .board .cell_have_black_piece (new_x ,new_y ):
                    move =Move (pawn ,x ,y ,new_x ,new_y )
                    move .is_capture =True 
                    move .captured_piece =self .board .get_piece_with_coordinates (new_x ,new_y )
                    if new_y ==0 :
                        move .promotion_piece ='queen'
                    moves .append (move )
                elif pawn .color =='Black'and self .board .cell_have_white_piece (new_x ,new_y ):
                    move =Move (pawn ,x ,y ,new_x ,new_y )
                    move .is_capture =True 
                    move .captured_piece =self .board .get_piece_with_coordinates (new_x ,new_y )
                    if new_y ==7 :
                        move .promotion_piece ='queen'
                    moves .append (move )


        if game_state and game_state .en_passant_target :
            ep_x ,ep_y =game_state .en_passant_target 

            if (pawn .color =='White'and y ==3 and ep_y ==2 and abs (x -ep_x )==1 )or (pawn .color =='Black'and y ==4 and ep_y ==5 and abs (x -ep_x )==1 ):
                move =Move (pawn ,x ,y ,ep_x ,ep_y )
                move .is_capture =True 
                move .is_en_passant =True 
                move .captured_piece =game_state .en_passant_pawn 
                moves .append (move )

        return moves 

    def generate_knight_moves (self ,knight ):
        """Sinh nước đi cho mã"""
        moves =[]
        x ,y =knight .current_coordinates 
        knight_offsets =[(1 ,2 ),(2 ,1 ),(2 ,-1 ),(1 ,-2 ),
        (-1 ,-2 ),(-2 ,-1 ),(-2 ,1 ),(-1 ,2 )]

        for dx ,dy in knight_offsets :
            new_x ,new_y =x +dx ,y +dy 
            if is_valid_position (new_x ,new_y ):
                if self .board .cell_is_empty (new_x ,new_y ):
                    moves .append (Move (knight ,x ,y ,new_x ,new_y ))
                else :

                    target_piece =self .board .get_piece_with_coordinates (new_x ,new_y )
                    if target_piece and target_piece .color !=knight .color :
                        move =Move (knight ,x ,y ,new_x ,new_y )
                        move .is_capture =True 
                        move .captured_piece =target_piece 
                        moves .append (move )

        return moves 

    def generate_bishop_moves (self ,bishop ):
        """Sinh nước đi cho tượng"""
        return self .generate_sliding_moves (bishop ,[(1 ,1 ),(1 ,-1 ),(-1 ,1 ),(-1 ,-1 )])

    def generate_rook_moves (self ,rook ):
        """Sinh nước đi cho xe"""
        return self .generate_sliding_moves (rook ,[(0 ,1 ),(0 ,-1 ),(1 ,0 ),(-1 ,0 )])

    def generate_queen_moves (self ,queen ):
        """Sinh nước đi cho hậu"""
        directions =[(0 ,1 ),(0 ,-1 ),(1 ,0 ),(-1 ,0 ),
        (1 ,1 ),(1 ,-1 ),(-1 ,1 ),(-1 ,-1 )]
        return self .generate_sliding_moves (queen ,directions )

    def generate_sliding_moves (self ,piece ,directions ):
        """
        Sinh nước đi cho các quân di chuyển theo đường thẳng (xe, tượng, hậu)
        """
        moves =[]
        x ,y =piece .current_coordinates 

        for dx ,dy in directions :
            new_x ,new_y =x +dx ,y +dy 
            while is_valid_position (new_x ,new_y ):
                if self .board .cell_is_empty (new_x ,new_y ):
                    moves .append (Move (piece ,x ,y ,new_x ,new_y ))
                else :

                    target_piece =self .board .get_piece_with_coordinates (new_x ,new_y )
                    if target_piece .color !=piece .color :

                        move =Move (piece ,x ,y ,new_x ,new_y )
                        move .is_capture =True 
                        move .captured_piece =target_piece 
                        moves .append (move )
                    break 

                new_x +=dx 
                new_y +=dy 

        return moves 

    def generate_king_moves (self ,king ):
        """Sinh nước đi cho vua"""
        moves =[]
        x ,y =king .current_coordinates 


        for dx in [-1 ,0 ,1 ]:
            for dy in [-1 ,0 ,1 ]:
                if dx ==0 and dy ==0 :
                    continue 
                new_x ,new_y =x +dx ,y +dy 
                if is_valid_position (new_x ,new_y ):
                    if self .board .cell_is_empty (new_x ,new_y ):
                        moves .append (Move (king ,x ,y ,new_x ,new_y ))
                    else :
                        target_piece =self .board .get_piece_with_coordinates (new_x ,new_y )
                        if target_piece and target_piece .color !=king .color :
                            move =Move (king ,x ,y ,new_x ,new_y )
                            move .is_capture =True 
                            move .captured_piece =target_piece 
                            moves .append (move )

        return moves 

    def generate_castling_moves (self ,king ,game_state ):
        """
        Sinh nước nhập thành
        
        Args:
            king: Quân vua
            game_state: GameState object
        """
        moves =[]
        color =king .color 
        x ,y =king .current_coordinates 


        if king .had_move ()or game_state .check_for_check (color ):
            return moves 


        if game_state .castling_rights [color ]['kingside']:
            if self .can_castle_kingside (king ,game_state ):
                move =Move (king ,x ,y ,x +2 ,y )
                move .is_castling =True 
                moves .append (move )


        if game_state .castling_rights [color ]['queenside']:
            if self .can_castle_queenside (king ,game_state ):
                move =Move (king ,x ,y ,x -2 ,y )
                move .is_castling =True 
                moves .append (move )

        return moves 

    def can_castle_kingside (self ,king ,game_state ):
        """Kiểm tra có thể nhập thành phía vua không"""
        x ,y =king .current_coordinates 


        for check_x in [x +1 ,x +2 ]:
            if not self .board .cell_is_empty (check_x ,y ):
                return False 


        rook =self .board .get_piece_with_coordinates (7 ,y )
        if not rook or rook .role !='rook'or rook .had_move ():
            return False 


        for check_x in [x ,x +1 ,x +2 ]:
            if self .is_square_attacked (check_x ,y ,king .color ,game_state ):
                return False 

        return True 

    def can_castle_queenside (self ,king ,game_state ):
        """Kiểm tra có thể nhập thành phía hậu không"""
        x ,y =king .current_coordinates 


        for check_x in [x -1 ,x -2 ,x -3 ]:
            if not self .board .cell_is_empty (check_x ,y ):
                return False 


        rook =self .board .get_piece_with_coordinates (0 ,y )
        if not rook or rook .role !='rook'or rook .had_move ():
            return False 


        for check_x in [x ,x -1 ,x -2 ]:
            if self .is_square_attacked (check_x ,y ,king .color ,game_state ):
                return False 

        return True 

    def is_square_attacked (self ,x ,y ,color ,game_state ):
        """
        Kiểm tra ô (x,y) có bị quân địch tấn công không
        
        Args:
            x, y: Tọa độ ô cần kiểm tra
            color: Màu của quân đang kiểm tra (vua)
            game_state: GameState object
        """
        opponent_color ='Black'if color =='White'else 'White'

        for piece in self .board .pieces :
            if piece .color ==opponent_color :
                moves =self .generate_pseudo_legal_moves (piece )
                for move in moves :
                    if move .to_x ==x and move .to_y ==y :
                        return True 
        return False 

    def generate_all_legal_moves (self ,color ,game_state ):
        """
        Sinh tất cả nước đi hợp lệ (đã kiểm tra vua không bị chiếu)
        
        Args:
            color: 'White' hoặc 'Black'
            game_state: GameState object
        
        Returns:
            List[Move]: Danh sách nước đi hợp lệ
        """
        pseudo_legal_moves =self .generate_all_moves (color ,game_state )
        legal_moves =[]

        for move in pseudo_legal_moves :
            if self .is_legal_move (move ,game_state ):
                legal_moves .append (move )


        for piece in self .board .pieces :
            if piece .color ==color and piece .role =='king':
                castling_moves =self .generate_castling_moves (piece ,game_state )
                legal_moves .extend (castling_moves )

        return legal_moves 

    def is_legal_move (self ,move ,game_state ):
        """
        Kiểm tra nước đi có hợp lệ không (không để vua bị chiếu)
        
        Args:
            move: Move object
            game_state: GameState object
        
        Returns:
            bool: True nếu hợp lệ
        """

        target_piece =None 
        if move .is_capture :
            target_piece =self .board .get_piece_with_coordinates (move .to_x ,move .to_y )
            if target_piece and target_piece .role =='king':
                return False 


        board_copy =copy_board (self .board )


        piece_copy =board_copy .get_piece_with_coordinates (
        move .from_x ,move .from_y 
        )

        if move .is_capture and not move .is_en_passant :
            captured_copy =board_copy .get_piece_with_coordinates (
            move .to_x ,move .to_y 
            )
            if captured_copy :
                board_copy .remove_piece (captured_copy )


        if move .is_en_passant and move .captured_piece :
            captured_x =move .captured_piece .current_coordinates [0 ]
            captured_y =move .captured_piece .current_coordinates [1 ]
            captured_copy =board_copy .get_piece_with_coordinates (captured_x ,captured_y )
            if captured_copy :
                board_copy .remove_piece (captured_copy )

        piece_copy .set_coordinate (move .to_x ,move .to_y )


        board_copy .update_all_coordinates ()


        temp_game_state =type (game_state )(board_copy )
        is_check =temp_game_state .check_for_check (move .piece .color )

        return not is_check 