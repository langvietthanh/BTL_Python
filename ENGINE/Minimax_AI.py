

import time 
import random 
import copy 
from ENGINE .Board_Evaluator import BoardEvaluator 
from ENGINE .Move_Generator import MoveGenerator ,copy_board 
from UTILS .Constants import AI_CONFIG 

class MinimaxAI :
    def __init__ (self ,difficulty ='medium'):
        """
        Khởi tạo Minimax AI
        
        Args:
            difficulty: 'easy', 'medium', 'hard'
        """
        self .difficulty =difficulty 
        self .config =AI_CONFIG [difficulty ]
        self .depth =self .config ['depth']
        self .time_limit =self .config ['time_limit']
        self .randomness =self .config ['randomness']

        self .evaluator =BoardEvaluator ()
        self .nodes_evaluated =0 
        self .best_move =None 
        self .start_time =None 

    def find_best_move (self ,board ,game_state ,color ):
        """
        Tìm nước đi tốt nhất cho màu này
        
        Args:
            board: Chess_Board object
            game_state: GameState object
            color: 'White' hoặc 'Black'
        
        Returns:
            Move: Nước đi tốt nhất
        """
        self .nodes_evaluated =0 
        self .best_move =None 
        self .start_time =time .time ()


        move_gen =MoveGenerator (board )
        legal_moves =move_gen .generate_all_legal_moves (color ,game_state )

        if not legal_moves :
            return None 


        legal_moves =self .order_moves (legal_moves ,board )


        if random .random ()<self .randomness :
            return random .choice (legal_moves )


        best_move =None 
        for current_depth in range (1 ,self .depth +1 ):

            if time .time ()-self .start_time >self .time_limit :
                break 

            best_score =float ('-inf')if color =='White'else float ('inf')
            current_best =None 

            for move in legal_moves :

                board_copy =copy_board (board )
                self .make_move (board_copy ,move )


                from MODEL .Game_State import GameState 
                new_game_state =GameState (board_copy )
                new_game_state .current_turn ='Black'if color =='White'else 'White'


                if color =='White':
                    score =self .minimax (board_copy ,new_game_state ,current_depth -1 ,
                    float ('-inf'),float ('inf'),False )
                    if score >best_score :
                        best_score =score 
                        current_best =move 
                else :
                    score =self .minimax (board_copy ,new_game_state ,current_depth -1 ,
                    float ('-inf'),float ('inf'),True )
                    if score <best_score :
                        best_score =score 
                        current_best =move 


                if time .time ()-self .start_time >self .time_limit :
                    break 

            if current_best :
                best_move =current_best 

        print (f"AI evaluated {self .nodes_evaluated } positions in {time .time ()-self .start_time :.2f}s")
        return best_move 

    def minimax (self ,board ,game_state ,depth ,alpha ,beta ,is_maximizing ):
        """
        Thuật toán Minimax với Alpha-Beta Pruning
        
        Args:
            board: Bàn cờ hiện tại
            game_state: Trạng thái game
            depth: Độ sâu còn lại
            alpha: Giá trị alpha (best cho Max)
            beta: Giá trị beta (best cho Min)
            is_maximizing: True nếu đang maximize (White), False nếu minimize (Black)
        
        Returns:
            float: Điểm đánh giá tốt nhất
        """
        self .nodes_evaluated +=1 


        if time .time ()-self .start_time >self .time_limit :
            return self .evaluator .quick_evaluate (board )


        if depth ==0 or game_state .game_over :
            return self .evaluator .evaluate (board ,game_state )

        move_gen =MoveGenerator (board )
        color ='White'if is_maximizing else 'Black'
        legal_moves =move_gen .generate_all_legal_moves (color ,game_state )


        if not legal_moves :
            return self .evaluator .evaluate (board ,game_state )


        legal_moves =self .order_moves (legal_moves ,board )

        if is_maximizing :
            max_eval =float ('-inf')
            for move in legal_moves :
                board_copy =copy_board (board )
                self .make_move (board_copy ,move )

                from MODEL .Game_State import GameState 
                new_game_state =GameState (board_copy )
                new_game_state .current_turn ='Black'

                eval_score =self .minimax (board_copy ,new_game_state ,depth -1 ,
                alpha ,beta ,False )
                max_eval =max (max_eval ,eval_score )
                alpha =max (alpha ,eval_score )

                if beta <=alpha :
                    break 

            return max_eval 
        else :
            min_eval =float ('inf')
            for move in legal_moves :
                board_copy =copy_board (board )
                self .make_move (board_copy ,move )

                from MODEL .Game_State import GameState 
                new_game_state =GameState (board_copy )
                new_game_state .current_turn ='White'

                eval_score =self .minimax (board_copy ,new_game_state ,depth -1 ,
                alpha ,beta ,True )
                min_eval =min (min_eval ,eval_score )
                beta =min (beta ,eval_score )

                if beta <=alpha :
                    break 

            return min_eval 

    def order_moves (self ,moves ,board ):
        """
        Sắp xếp moves để tối ưu alpha-beta pruning
        Ưu tiên:
        1. Captures (ăn quân)
        2. Checks (chiếu)
        3. Moves khác
        """
        def move_priority (move ):
            priority =0 


            if move .is_capture and move .captured_piece :
                from UTILS .Constants import PIECE_VALUES 
                priority +=PIECE_VALUES .get (move .captured_piece .role ,0 )


                priority +=PIECE_VALUES .get (move .captured_piece .role ,0 )*10 
                priority -=PIECE_VALUES .get (move .piece .role ,0 )


            center_distance =abs (move .to_x -3.5 )+abs (move .to_y -3.5 )
            priority -=center_distance 

            return priority 

        return sorted (moves ,key =move_priority ,reverse =True )

    def make_move (self ,board ,move ):
        """
        Thực hiện nước đi trên bàn cờ
        
        Args:
            board: Chess_Board object
            move: Move object
        """

        if move .is_capture and not move .is_en_passant :
            captured_on_board =board .get_piece_with_coordinates (move .to_x ,move .to_y )
            if captured_on_board :
                board .remove_piece (captured_on_board )


        if move .is_en_passant and move .captured_piece :

            captured_x =move .captured_piece .current_coordinates [0 ]
            captured_y =move .captured_piece .current_coordinates [1 ]
            captured_on_board =board .get_piece_with_coordinates (captured_x ,captured_y )
            if captured_on_board :
                board .remove_piece (captured_on_board )


        piece =board .get_piece_with_coordinates (move .from_x ,move .from_y )
        if piece :
            piece .set_coordinate (move .to_x ,move .to_y )


        if move .is_castling :

            if move .to_x ==6 :
                rook =board .get_piece_with_coordinates (7 ,move .from_y )
                if rook :
                    rook .set_coordinate (5 ,move .from_y )
            else :
                rook =board .get_piece_with_coordinates (0 ,move .from_y )
                if rook :
                    rook .set_coordinate (3 ,move .from_y )


        if move .promotion_piece :

            import pygame as pg 
            piece =board .get_piece_with_coordinates (move .to_x ,move .to_y )
            if piece :

                piece .role =move .promotion_piece 


        board .update_all_coordinates ()

    def set_difficulty (self ,difficulty ):
        """
        Thay đổi độ khó
        """
        self .difficulty =difficulty 
        self .config =AI_CONFIG [difficulty ]
        self .depth =self .config ['depth']
        self .time_limit =self .config ['time_limit']
        self .randomness =self .config ['randomness']