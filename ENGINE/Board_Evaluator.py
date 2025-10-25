

from UTILS .Constants import *
from UTILS .Helper import is_endgame ,calculate_mobility ,flip_coordinate_for_black 

class BoardEvaluator :
    def __init__ (self ):
        pass 

    def evaluate (self ,board ,game_state ,color ='White'):
        """
        Đánh giá bàn cờ từ góc nhìn của White
        Điểm dương: White tốt hơn
        Điểm âm: Black tốt hơn
        
        Args:
            board: Chess_Board object
            game_state: GameState object
            color: Màu đang đánh giá
        
        Returns:
            float: Điểm đánh giá
        """

        if game_state .is_checkmate :
            if game_state .winner =='White':
                return 100000 
            else :
                return -100000 

        if game_state .is_stalemate or game_state .is_draw :
            return 0 

        score =0 


        score +=self .evaluate_material (board )


        score +=self .evaluate_piece_positions (board ,game_state )


        score +=self .evaluate_king_safety (board ,game_state )


        score +=self .evaluate_mobility (board )


        score +=self .evaluate_pawn_structure (board )


        score +=self .evaluate_center_control (board )

        return score 

    def evaluate_material (self ,board ):
        """
        Đánh giá giá trị vật chất
        """
        score =0 
        for piece in board .pieces :
            value =PIECE_VALUES .get (piece .role ,0 )
            if piece .color =='White':
                score +=value 
            else :
                score -=value 
        return score 

    def evaluate_piece_positions (self ,board ,game_state ):
        """
        Đánh giá vị trí của các quân dựa trên piece-square tables
        """
        score =0 
        is_end_game =is_endgame (board )

        for piece in board .pieces :
            x ,y =piece .current_coordinates 


            if piece .role =='king'and is_end_game :
                table =KING_END_GAME_TABLE 
            else :
                table =PIECE_SQUARE_TABLES .get (piece .role )

            if table :

                if piece .color =='Black':
                    x_flipped ,y_flipped =flip_coordinate_for_black (x ,y )
                    position_value =table [y_flipped ][x_flipped ]
                else :
                    position_value =table [y ][x ]

                if piece .color =='White':
                    score +=position_value 
                else :
                    score -=position_value 

        return score 

    def evaluate_king_safety (self ,board ,game_state ):
        """
        Đánh giá độ an toàn của vua
        """
        score =0 


        white_king =None 
        black_king =None 
        for piece in board .pieces :
            if piece .role =='king':
                if piece .color =='White':
                    white_king =piece 
                else :
                    black_king =piece 

        if white_king :
            score +=self .king_safety_score (white_king ,board ,game_state )

        if black_king :
            score -=self .king_safety_score (black_king ,board ,game_state )

        return score 

    def king_safety_score (self ,king ,board ,game_state ):
        """
        Tính điểm an toàn cho một vua
        """
        safety_score =0 
        x ,y =king .current_coordinates 


        direction =-1 if king .color =='White'else 1 
        shield_positions =[
        [x -1 ,y +direction ],[x ,y +direction ],[x +1 ,y +direction ]
        ]

        for pos in shield_positions :
            if 0 <=pos [0 ]<=7 and 0 <=pos [1 ]<=7 :
                piece =board .get_piece_with_coordinates (pos [0 ],pos [1 ])
                if piece and piece .role =='pawn'and piece .color ==king .color :
                    safety_score +=10 


        if not is_endgame (board ):
            if 2 <=x <=5 and 2 <=y <=5 :
                safety_score -=30 


        if game_state .check_for_check (king .color ):
            safety_score -=50 

        return safety_score 

    def evaluate_mobility (self ,board ):
        """
        Đánh giá khả năng di chuyển (số nước đi có thể)
        """
        white_mobility =calculate_mobility (board ,'White')
        black_mobility =calculate_mobility (board ,'Black')


        return (white_mobility -black_mobility )

    def evaluate_pawn_structure (self ,board ):
        """
        Đánh giá cấu trúc tốt
        """
        score =0 


        white_pawns =[p for p in board .pieces if p .role =='pawn'and p .color =='White']
        black_pawns =[p for p in board .pieces if p .role =='pawn'and p .color =='Black']

        score +=self .pawn_structure_score (white_pawns )
        score -=self .pawn_structure_score (black_pawns )

        return score 

    def pawn_structure_score (self ,pawns ):
        """
        Tính điểm cấu trúc tốt
        """
        if not pawns :
            return 0 

        score =0 
        pawn_files ={}

        for pawn in pawns :
            x ,y =pawn .current_coordinates 
            if x not in pawn_files :
                pawn_files [x ]=[]
            pawn_files [x ].append (y )


        for file ,ranks in pawn_files .items ():
            if len (ranks )>1 :
                score -=20 *(len (ranks )-1 )


        for file in pawn_files .keys ():
            has_neighbor =False 
            for neighbor_file in [file -1 ,file +1 ]:
                if neighbor_file in pawn_files :
                    has_neighbor =True 
                    break 
            if not has_neighbor :
                score -=15 


        for pawn in pawns :
            if self .is_passed_pawn (pawn ,pawns ):
                score +=30 


        for i ,pawn1 in enumerate (pawns ):
            for pawn2 in pawns [i +1 :]:
                x1 ,y1 =pawn1 .current_coordinates 
                x2 ,y2 =pawn2 .current_coordinates 
                if abs (x1 -x2 )==1 and abs (y1 -y2 )<=1 :
                    score +=10 

        return score 

    def is_passed_pawn (self ,pawn ,all_pawns ):
        """
        Kiểm tra tốt có phải tốt thông không (không có tốt địch chặn phía trước)
        """
        x ,y =pawn .current_coordinates 
        direction =-1 if pawn .color =='White'else 1 


        for check_file in [x -1 ,x ,x +1 ]:
            if 0 <=check_file <=7 :
                check_y =y +direction 
                while 0 <=check_y <=7 :

                    for other_pawn in all_pawns :
                        if other_pawn !=pawn :
                            ox ,oy =other_pawn .current_coordinates 
                            if ox ==check_file and oy ==check_y :
                                return False 
                    check_y +=direction 

        return True 

    def evaluate_center_control (self ,board ):
        """
        Đánh giá kiểm soát trung tâm (4 ô giữa)
        """
        score =0 
        center_squares =[[3 ,3 ],[3 ,4 ],[4 ,3 ],[4 ,4 ]]

        for x ,y in center_squares :
            piece =board .get_piece_with_coordinates (x ,y )
            if piece :
                if piece .color =='White':
                    score +=20 
                else :
                    score -=20 

        return score 

    def evaluate_development (self ,board ):
        """
        Đánh giá sự phát triển quân (khai cuộc)
        """
        score =0 


        for piece in board .pieces :
            if piece .role in ['knight','bishop']:
                x ,y =piece .current_coordinates 


                if piece .color =='White':
                    if y <7 :
                        score +=15 
                    if y <=4 :
                        score +=10 


                else :
                    if y >0 :
                        score -=15 
                    if y >=3 :
                        score -=10 

        return score 

    def quick_evaluate (self ,board ):
        """
        Đánh giá nhanh chỉ dựa trên material (dùng cho alpha-beta pruning)
        """
        score =0 
        for piece in board .pieces :
            value =PIECE_VALUES .get (piece .role ,0 )
            if piece .color =='White':
                score +=value 
            else :
                score -=value 
        return score 

    def evaluate_threats (self ,board ):
        """
        Đánh giá các mối đe dọa trên bàn cờ
        """
        score =0 


        for piece in board .pieces :
            attackers =self .count_attackers (piece ,board )
            defenders =self .count_defenders (piece ,board )

            if attackers >defenders :

                threat_value =PIECE_VALUES .get (piece .role ,0 )*0.1 
                if piece .color =='White':
                    score -=threat_value 
                else :
                    score +=threat_value 

        return score 

    def count_attackers (self ,piece ,board ):
        """Đếm số quân địch đang tấn công quân này"""
        count =0 
        opponent_color ='Black'if piece .color =='White'else 'White'
        x ,y =piece .current_coordinates 

        for attacker in board .pieces :
            if attacker .color ==opponent_color :

                attacker .set_valid_moves (board )
                if [x ,y ]in attacker .valid_moves :
                    count +=1 

        return count 

    def count_defenders (self ,piece ,board ):
        """Đếm số quân đồng minh đang bảo vệ quân này"""
        count =0 
        x ,y =piece .current_coordinates 

        for defender in board .pieces :
            if defender .color ==piece .color and defender !=piece :
                defender .set_valid_moves (board )
                if [x ,y ]in defender .valid_moves :
                    count +=1 

        return count 