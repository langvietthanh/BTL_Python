

import pygame as pg 
import time 
from MODEL .Game_State import GameState 
from ENGINE .AI_Controller import AIController 
from ENGINE .Move_Generator import MoveGenerator 

class GameController :
    def __init__ (self ,board ,board_view ,game_mode ='PVP',ai_difficulty ='medium'):
        """
        Khởi tạo Game Controller
        
        Args:
            board: Chess_Board object
            board_view: Board_View object
            game_mode: 'PVP', 'PVE'
            ai_difficulty: 'easy', 'medium', 'hard'
        """
        self .board =board 
        self .board_view =board_view 
        self .game_state =GameState (board )
        self .game_mode =game_mode 


        self .ai_controller =AIController (difficulty =ai_difficulty )
        self .ai_color ='Black'
        self .ai_thinking =False 


        self .move_generator =MoveGenerator (board )


        self .selected_piece =None 
        self .valid_moves =[]


        self .waiting_for_promotion =False 
        self .promotion_move =None 

    def handle_events (self ,event ):
        """
        Xử lý events từ pygame
        """

        if self .game_state .game_over :
            return 


        if self .ai_thinking :
            return 


        if self .waiting_for_promotion :
            self .handle_promotion_choice (event )
            return 


        if event .type ==pg .MOUSEBUTTONDOWN :
            self .handle_mouse_down (event )
        elif event .type ==pg .MOUSEMOTION :
            self .handle_mouse_motion (event )
        elif event .type ==pg .MOUSEBUTTONUP :
            self .handle_mouse_up (event )

    def handle_mouse_down (self ,event ):
        """Xử lý nhấn chuột"""

        if self .game_mode =='PVE'and self .game_state .current_turn ==self .ai_color :
            return 

        mouse_x ,mouse_y =event .pos 


        from UTILS .Constants import CELL_SIZE 
        board_x =mouse_x //CELL_SIZE 
        board_y =mouse_y //CELL_SIZE 


        logic_x ,logic_y =self .board_view .get_logic_coordinates (board_x ,board_y )


        for piece in self .board .pieces :

            if (piece .current_coordinates [0 ]==logic_x and 
            piece .current_coordinates [1 ]==logic_y ):

                if piece .color ==self .game_state .current_turn :
                    self .selected_piece =piece 
                    self .board_view .selected_piece =piece 


                    piece .offset [0 ]=piece .rect .x -mouse_x 
                    piece .offset [1 ]=piece .rect .y -mouse_y 


                    self .valid_moves =self .get_valid_moves_for_piece (piece )
                    break 

    def handle_mouse_motion (self ,event ):
        """Xử lý di chuyển chuột (drag)"""
        if self .selected_piece :
            mouse_x ,mouse_y =event .pos 
            self .selected_piece .rect .x =mouse_x +self .selected_piece .offset [0 ]
            self .selected_piece .rect .y =mouse_y +self .selected_piece .offset [1 ]

    def handle_mouse_up (self ,event ):
        """Xử lý thả chuột"""
        if not self .selected_piece :
            return 

        mouse_x ,mouse_y =event .pos 


        from UTILS .Constants import CELL_SIZE 
        target_x =mouse_x //CELL_SIZE 
        target_y =mouse_y //CELL_SIZE 


        target_x ,target_y =self .board_view .get_logic_coordinates (target_x ,target_y )


        valid_move =None 
        for move in self .valid_moves :
            if move .to_x ==target_x and move .to_y ==target_y :
                valid_move =move 
                break 

        if valid_move :

            if (valid_move .piece .role =='pawn'and 
            ((valid_move .piece .color =='White'and target_y ==0 )or 
            (valid_move .piece .color =='Black'and target_y ==7 ))):

                self .waiting_for_promotion =True 
                self .promotion_move =valid_move 

            else :

                self .execute_move (valid_move )
        else :

            self .selected_piece .set_rect ()


        self .selected_piece =None 
        self .board_view .selected_piece =None 
        self .valid_moves =[]

    def get_valid_moves_for_piece (self ,piece ):
        """
        Lấy tất cả nước đi hợp lệ cho quân cờ
        """
        legal_moves =self .move_generator .generate_all_legal_moves (
        piece .color ,self .game_state 
        )


        piece_moves =[]
        for move in legal_moves :
            if (move .from_x ==piece .current_coordinates [0 ]and 
            move .from_y ==piece .current_coordinates [1 ]):
                piece_moves .append (move )

        return piece_moves 

    def execute_move (self ,move ):
        """
        Thực hiện nước đi và cập nhật game state
        """

        if move .is_capture and move .captured_piece :
            self .game_state .captured_pieces [move .captured_piece .color ].append (
            move .captured_piece 
            )

            if not move .is_en_passant :
                self .board .remove_piece (move .captured_piece )


        if move .is_en_passant and move .captured_piece :

            captured_x =move .captured_piece .current_coordinates [0 ]
            captured_y =move .captured_piece .current_coordinates [1 ]
            self .board .remove_piece (move .captured_piece )


        piece =self .board .get_piece_with_coordinates (move .from_x ,move .from_y )
        piece .set_coordinate (move .to_x ,move .to_y )


        if move .is_castling :
            if move .to_x ==6 :
                rook =self .board .get_piece_with_coordinates (7 ,move .from_y )
                if rook :
                    rook .set_coordinate (5 ,move .from_y )
            else :
                rook =self .board .get_piece_with_coordinates (0 ,move .from_y )
                if rook :
                    rook .set_coordinate (3 ,move .from_y )


        if move .promotion_piece :
            self .promote_pawn (piece ,move .promotion_piece )


        self .game_state .add_move_to_history (move )
        self .game_state .update_castling_rights (move )
        self .game_state .update_en_passant (move )


        self .board .update_all_coordinates ()


        self .game_state .switch_turn ()


        self .game_state .update_game_state ()


        if (self .game_mode =='PVE'and 
        self .game_state .current_turn ==self .ai_color and 
        not self .game_state .game_over ):
            self .ai_thinking =True 

    def update_ai (self ):
        """
        Gọi AI để đi nước (non-blocking nếu có thể)
        """
        if not self .ai_thinking or self .game_state .game_over :
            return 


        ai_move =self .ai_controller .get_ai_move (
        self .board ,
        self .game_state ,
        self .game_state .current_turn 
        )

        if ai_move :

            self .execute_move (ai_move )

        self .ai_thinking =False 

    def promote_pawn (self ,pawn ,promotion_piece ):
        """
        Phong cấp tốt
        """
        import pygame as pg 
        from UTILS .Constants import CELL_SIZE 


        pawn .role =promotion_piece 


        piece_images ={
        'queen':f'PNG/{pawn .color .lower ()}_queen.png',
        'rook':f'PNG/{pawn .color .lower ()}_rook.png',
        'bishop':f'PNG/{pawn .color .lower ()}_bishop.png',
        'knight':f'PNG/{pawn .color .lower ()}_knight.png',
        }

        if promotion_piece in piece_images :
            try :
                new_img =pg .image .load (piece_images [promotion_piece ])
                pawn .img =pg .transform .scale (new_img ,(100 ,100 ))

                pawn .rect =pawn .img .get_rect (
                topleft =(pawn .current_coordinates [0 ]*CELL_SIZE ,
                pawn .current_coordinates [1 ]*CELL_SIZE )
                )
            except :
                pass 

    def handle_promotion_choice (self ,event ):
        """
        Xử lý lựa chọn quân phong cấp bằng chuột
        """
        from UTILS .Constants import BOARD_SIZE ,CELL_SIZE 

        if event .type ==pg .MOUSEBUTTONDOWN :
            mouse_x ,mouse_y =event .pos 


            board_center_x =BOARD_SIZE *CELL_SIZE //2 
            board_center_y =BOARD_SIZE *CELL_SIZE //2 


            button_size =60 
            button_spacing =80 


            buttons ={
            'queen':(board_center_x -1.5 *button_spacing ,board_center_y -button_size //2 ),
            'rook':(board_center_x -0.5 *button_spacing ,board_center_y -button_size //2 ),
            'bishop':(board_center_x +0.5 *button_spacing ,board_center_y -button_size //2 ),
            'knight':(board_center_x +1.5 *button_spacing ,board_center_y -button_size //2 )
            }


            for piece_type ,(btn_x ,btn_y )in buttons .items ():
                if (btn_x <=mouse_x <=btn_x +button_size and 
                btn_y <=mouse_y <=btn_y +button_size ):

                    if self .promotion_move :
                        self .promotion_move .promotion_piece =piece_type 
                        self .execute_move (self .promotion_move )


                        self .waiting_for_promotion =False 
                        self .promotion_move =None 
                    break 

    def draw_promotion_selection (self ,screen ):
        """
        Vẽ UI lựa chọn phong cấp
        """
        from UTILS .Constants import BOARD_SIZE ,CELL_SIZE 

        if not self .waiting_for_promotion :
            return 


        overlay =pg .Surface ((BOARD_SIZE *CELL_SIZE ,BOARD_SIZE *CELL_SIZE ))
        overlay .set_alpha (180 )
        overlay .fill ((0 ,0 ,0 ))
        screen .blit (overlay ,(0 ,0 ))


        board_center_x =BOARD_SIZE *CELL_SIZE //2 
        board_center_y =BOARD_SIZE *CELL_SIZE //2 

        button_size =60 
        button_spacing =80 


        font =pg .font .Font (None ,24 )


        buttons ={
        'queen':(board_center_x -1.5 *button_spacing ,board_center_y -button_size //2 ),
        'rook':(board_center_x -0.5 *button_spacing ,board_center_y -button_size //2 ),
        'bishop':(board_center_x +0.5 *button_spacing ,board_center_y -button_size //2 ),
        'knight':(board_center_x +1.5 *button_spacing ,board_center_y -button_size //2 )
        }


        for piece_type ,(btn_x ,btn_y )in buttons .items ():

            button_rect =pg .Rect (btn_x ,btn_y ,button_size ,button_size )
            pg .draw .rect (screen ,(255 ,255 ,255 ),button_rect )
            pg .draw .rect (screen ,(0 ,0 ,0 ),button_rect ,3 )


            piece_images ={
            'queen':f'PNG/{self .promotion_move .piece .color .lower ()}_queen.png',
            'rook':f'PNG/{self .promotion_move .piece .color .lower ()}_rook.png',
            'bishop':f'PNG/{self .promotion_move .piece .color .lower ()}_bishop.png',
            'knight':f'PNG/{self .promotion_move .piece .color .lower ()}_knight.png'
            }

            if piece_type in piece_images :
                try :
                    piece_img =pg .image .load (piece_images [piece_type ])
                    piece_img =pg .transform .scale (piece_img ,(button_size -10 ,button_size -10 ))


                    img_x =btn_x +(button_size -piece_img .get_width ())//2 
                    img_y =btn_y +(button_size -piece_img .get_height ())//2 

                    screen .blit (piece_img ,(img_x ,img_y ))
                except :

                    piece_symbols ={
                    'queen':'♕',
                    'rook':'♖',
                    'bishop':'♗',
                    'knight':'♘'
                    }
                    symbol_text =font .render (piece_symbols [piece_type ],True ,(0 ,0 ,0 ))
                    symbol_rect =symbol_text .get_rect (center =(btn_x +button_size //2 ,btn_y +button_size //2 ))
                    screen .blit (symbol_text ,symbol_rect )


        title_font =pg .font .Font (None ,36 )
        title_text =title_font .render ("Choose Promotion Piece",True ,(255 ,255 ,255 ))
        title_rect =title_text .get_rect (center =(board_center_x ,board_center_y -80 ))
        screen .blit (title_text ,title_rect )

    def reset_game (self ):
        """
        Reset game về trạng thái ban đầu
        """

        self .board .pieces .clear ()


        self .board_view .init_piece ()


        self .game_state .reset ()


        self .selected_piece =None 
        self .board_view .selected_piece =None 
        self .valid_moves =[]
        self .ai_thinking =False 

    def set_game_mode (self ,mode ,ai_color ='Black'):
        """
        Đặt chế độ chơi
        
        Args:
            mode: 'PVP', 'PVE'
            ai_color: 'White' hoặc 'Black' (cho PVE mode)
        """
        self .game_mode =mode 
        self .ai_color =ai_color 


        if (mode =='PVE'and self .game_state .current_turn ==ai_color ):
            self .ai_thinking =True 

    def set_ai_difficulty (self ,difficulty ):
        """Đặt độ khó AI"""
        self .ai_controller .set_difficulty (difficulty )

    def get_game_info (self ):
        """Lấy thông tin game để hiển thị"""
        return {
        'current_turn':self .game_state .current_turn ,
        'status':self .game_state .get_game_status (),
        'move_count':len (self .game_state .move_history ),
        'captured_white':self .game_state .captured_pieces ['White'],
        'captured_black':self .game_state .captured_pieces ['Black'],
        'is_check':self .game_state .is_check ,
        'game_over':self .game_state .game_over ,
        'winner':self .game_state .winner 
        }

    def undo_move (self ):
        """
        Hoàn tác nước đi cuối (bonus feature)
        """
        if len (self .game_state .move_history )==0 :
            return False 



        return False 

    def undo_move (self ):
        """
        Hoàn tác nước đi cuối cùng
        """
        if len (self .game_state .move_history )==0 :
            return False 


        last_move =self .game_state .move_history [-1 ]


        moved_piece =None 
        for piece in self .board .pieces :
            if (piece .current_coordinates [0 ]==last_move .to_x and 
            piece .current_coordinates [1 ]==last_move .to_y ):
                moved_piece =piece 
                break 

        if not moved_piece :
            return False 


        moved_piece .set_coordinate (last_move .from_x ,last_move .from_y )


        if last_move .is_capture and last_move .captured_piece :

            self .board .add_piece (last_move .captured_piece )

            if last_move .captured_piece in self .game_state .captured_pieces [last_move .captured_piece .color ]:
                self .game_state .captured_pieces [last_move .captured_piece .color ].remove (last_move .captured_piece )


        self .game_state .move_history .pop ()


        self .game_state .switch_turn ()


        self .board .update_all_coordinates ()


        self .game_state .update_game_state ()


        self .selected_piece =None 
        self .board_view .selected_piece =None 
        self .valid_moves =[]

        return True 