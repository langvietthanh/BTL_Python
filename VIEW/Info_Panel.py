

import pygame as pg 
import time 
from UTILS .Constants import *
from UTILS .Helper import move_to_notation ,piece_symbol_unicode 

class InfoPanel :
    def __init__ (self ,screen ,x ,y ,width ,height ):
        """
        Khởi tạo Info Panel đầy đủ
        
        Args:
            screen: Pygame screen
            x, y: Vị trí góc trên trái của panel
            width, height: Kích thước panel
        """
        self .screen =screen 
        self .rect =pg .Rect (x ,y ,width ,height )


        self .font_large =pg .font .Font (None ,FONT_LARGE )
        self .font_medium =pg .font .Font (None ,FONT_MEDIUM )
        self .font_small =pg .font .Font (None ,FONT_SMALL )


        self .scroll_offset =0 
        self .max_visible_moves =15 
        self .animation_time =0 


        self .header_height =100 
        self .status_height =120 
        self .captured_height =140 
        self .history_start =self .header_height +self .status_height +self .captured_height 

    def draw (self ,game_info ,move_history ,ai_thinking =False ):
        """
        Vẽ toàn bộ info panel
        
        Args:
            game_info: Dictionary thông tin game
            move_history: List các Move đã đi
            ai_thinking: AI có đang suy nghĩ không
        """

        pg .draw .rect (self .screen ,UI_BACKGROUND ,self .rect )
        pg .draw .rect (self .screen ,UI_TEXT ,self .rect ,3 )

        y_offset =self .rect .y +10 


        y_offset =self .draw_header (y_offset )


        y_offset =self .draw_status_section (game_info ,y_offset ,ai_thinking )


        y_offset =self .draw_captured_section (game_info ,y_offset )


        pg .draw .line (self .screen ,UI_TEXT ,
        (self .rect .x +10 ,y_offset ),
        (self .rect .right -10 ,y_offset ),2 )
        y_offset +=10 


        y_offset =self .draw_move_history_section (move_history ,y_offset )


        if ai_thinking :
            self .draw_ai_thinking_overlay ()


        self .draw_control_buttons ()


        if game_info .get ('game_over',False ):
            self .draw_game_over_overlay (game_info )

    def draw_header (self ,y_offset ):
        """
        Vẽ header panel
        
        Returns:
            int: Y offset tiếp theo
        """
        x_margin =self .rect .x +20 


        title =self .font_large .render ("♔ INFORMATION",True ,(255 ,215 ,0 ))
        title_rect =title .get_rect (center =(self .rect .centerx ,y_offset +25 ))
        self .screen .blit (title ,title_rect )


        subtitle =self .font_small .render ("Chess AI Game",True ,(150 ,150 ,150 ))
        subtitle_rect =subtitle .get_rect (center =(self .rect .centerx ,y_offset +55 ))
        self .screen .blit (subtitle ,subtitle_rect )


        y_offset +=80 
        pg .draw .line (self .screen ,UI_TEXT ,
        (self .rect .x +10 ,y_offset ),
        (self .rect .right -10 ,y_offset ),2 )

        return y_offset +10 

    def draw_status_section (self ,game_info ,y_offset ,ai_thinking ):
        """
        Vẽ phần trạng thái game
        
        Returns:
            int: Y offset tiếp theo
        """
        x_margin =self .rect .x +20 


        turn =game_info .get ('current_turn','White')
        turn_color =(255 ,255 ,255 )if turn =='White'else (50 ,50 ,50 )
        turn_bg =(50 ,50 ,50 )if turn =='White'else (200 ,200 ,200 )


        turn_box =pg .Rect (x_margin ,y_offset ,self .rect .width -40 ,35 )
        pg .draw .rect (self .screen ,turn_bg ,turn_box ,border_radius =5 )
        pg .draw .rect (self .screen ,turn_color ,turn_box ,2 ,border_radius =5 )

        turn_text =f"TURN: {turn .upper ()}"
        turn_surf =self .font_medium .render (turn_text ,True ,turn_color )
        turn_rect =turn_surf .get_rect (center =turn_box .center )
        self .screen .blit (turn_surf ,turn_rect )
        y_offset +=45 


        status =game_info .get ('status','')
        is_check =game_info .get ('is_check',False )
        status_color =HIGHLIGHT_CHECK if is_check else (200 ,200 ,200 )


        if is_check :
            status_icon ="⚠ "
        elif game_info .get ('game_over',False ):
            status_icon ="★ "
        else :
            status_icon ="● "

        status_text =status_icon +status 
        status_surf =self .font_small .render (status_text ,True ,status_color )
        self .screen .blit (status_surf ,(x_margin ,y_offset ))
        y_offset +=30 


        move_count =game_info .get ('move_count',0 )
        move_text =f"Moves: {move_count }"
        move_surf =self .font_small .render (move_text ,True ,UI_TEXT )
        self .screen .blit (move_surf ,(x_margin ,y_offset ))


        if ai_thinking :
            ai_text =self .get_thinking_animation ()
            ai_surf =self .font_small .render (ai_text ,True ,(255 ,255 ,0 ))
            ai_rect =ai_surf .get_rect (right =self .rect .right -25 ,centery =y_offset +7 )
            self .screen .blit (ai_surf ,ai_rect )

        y_offset +=30 

        return y_offset 

    def draw_captured_section (self ,game_info ,y_offset ):
        """
        Vẽ phần quân bị bắt với hiển thị chi tiết
        
        Returns:
            int: Y offset tiếp theo
        """
        x_margin =self .rect .x +20 


        title =self .font_medium .render ("Captured Pieces",True ,UI_TEXT )
        self .screen .blit (title ,(x_margin ,y_offset ))
        y_offset +=30 


        white_captured =game_info .get ('captured_white',[])
        y_offset =self .draw_captured_pieces_detail (
        white_captured ,"White",(255 ,255 ,255 ),x_margin ,y_offset 
        )

        y_offset +=5 


        black_captured =game_info .get ('captured_black',[])
        y_offset =self .draw_captured_pieces_detail (
        black_captured ,"Black",(80 ,80 ,80 ),x_margin ,y_offset 
        )

        y_offset +=10 


        white_value ,black_value =self .calculate_material_value (white_captured ,black_captured )
        advantage =white_value -black_value 

        if advantage >0 :
            adv_text =f"Black ahead: +{advantage }"
            adv_color =(100 ,255 ,100 )
        elif advantage <0 :
            adv_text =f"White ahead: +{abs (advantage )}"
            adv_color =(100 ,255 ,100 )
        else :
            adv_text ="Even"
            adv_color =(200 ,200 ,200 )

        adv_surf =self .font_small .render (adv_text ,True ,adv_color )
        self .screen .blit (adv_surf ,(x_margin ,y_offset ))
        y_offset +=25 

        return y_offset 

    def draw_captured_pieces_detail (self ,captured_pieces ,label ,color ,x ,y ):
        """
        Vẽ chi tiết quân bị bắt cho một màu
        
        Returns:
            int: Y offset tiếp theo
        """
        if not captured_pieces :

            text =f"{label }: -"
            surf =self .font_small .render (text ,True ,(120 ,120 ,120 ))
            self .screen .blit (surf ,(x ,y ))
            return y +22 


        label_text =f"{label } ({len (captured_pieces )}):"
        label_surf =self .font_small .render (label_text ,True ,color )
        self .screen .blit (label_surf ,(x ,y ))
        y +=20 


        piece_count ={}
        piece_symbols ={
        'pawn':'♟',
        'knight':'♞',
        'bishop':'♝',
        'rook':'♜',
        'queen':'♛',
        'king':'♚'
        }

        for piece in captured_pieces :
            role =piece .role 
            piece_count [role ]=piece_count .get (role ,0 )+1 


        piece_display =[]
        for role in ['queen','rook','bishop','knight','pawn']:
            if role in piece_count :
                count =piece_count [role ]
                symbol =piece_symbols .get (role ,'?')
                if count >1 :
                    piece_display .append (f"{symbol }×{count }")
                else :
                    piece_display .append (symbol )

        pieces_text ="  ".join (piece_display )
        pieces_surf =self .font_small .render (pieces_text ,True ,color )
        self .screen .blit (pieces_surf ,(x +10 ,y ))

        return y +22 

    def calculate_material_value (self ,white_captured ,black_captured ):
        """
        Tính giá trị vật chất đã mất
        
        Returns:
            tuple: (white_value, black_value)
        """
        values ={'pawn':1 ,'knight':3 ,'bishop':3 ,'rook':5 ,'queen':9 }

        white_value =sum (values .get (p .role ,0 )for p in white_captured )
        black_value =sum (values .get (p .role ,0 )for p in black_captured )

        return white_value ,black_value 

    def draw_move_history_section (self ,move_history ,y_offset ):
        """
        Vẽ phần lịch sử nước đi với scroll
        
        Returns:
            int: Y offset tiếp theo
        """
        x_margin =self .rect .x +20 


        title =self .font_medium .render ("Move History",True ,UI_TEXT )
        self .screen .blit (title ,(x_margin ,y_offset ))
        y_offset +=30 

        if not move_history :
            no_moves =self .font_small .render ("No moves yet",True ,(120 ,120 ,120 ))
            self .screen .blit (no_moves ,(x_margin ,y_offset ))
            return y_offset +25 


        history_area_height =self .rect .bottom -y_offset -20 
        visible_start =max (0 ,len (move_history )-self .max_visible_moves -self .scroll_offset )
        visible_end =min (len (move_history ),visible_start +self .max_visible_moves )
        visible_moves =move_history [visible_start :visible_end ]


        move_number =(visible_start //2 )+1 


        for i in range (0 ,len (visible_moves ),2 ):

            move_num_text =f"{move_number }."
            move_num_surf =self .font_small .render (move_num_text ,True ,(150 ,150 ,150 ))
            self .screen .blit (move_num_surf ,(x_margin ,y_offset ))


            white_move =visible_moves [i ]
            white_notation =move_to_notation (white_move )


            if white_move .is_checkmate :
                white_color =(255 ,0 ,0 )
            elif white_move .is_check :
                white_color =(255 ,165 ,0 )
            elif white_move .is_capture :
                white_color =(255 ,255 ,100 )
            else :
                white_color =UI_TEXT 

            white_surf =self .font_small .render (white_notation ,True ,white_color )
            self .screen .blit (white_surf ,(x_margin +35 ,y_offset ))


            if i +1 <len (visible_moves ):
                black_move =visible_moves [i +1 ]
                black_notation =move_to_notation (black_move )

                if black_move .is_checkmate :
                    black_color =(255 ,0 ,0 )
                elif black_move .is_check :
                    black_color =(255 ,165 ,0 )
                elif black_move .is_capture :
                    black_color =(255 ,255 ,100 )
                else :
                    black_color =UI_TEXT 

                black_surf =self .font_small .render (black_notation ,True ,black_color )
                self .screen .blit (black_surf ,(x_margin +120 ,y_offset ))


            if i +1 >=len (visible_moves )-1 :
                highlight_rect =pg .Rect (x_margin -5 ,y_offset -2 ,
                self .rect .width -30 ,20 )
                pg .draw .rect (self .screen ,(60 ,60 ,60 ),highlight_rect ,1 )

            y_offset +=22 
            move_number +=1 


            if y_offset >self .rect .bottom -30 :
                break 


        if visible_start >0 :

            up_arrow ="▲ Scroll up"
            up_surf =self .font_small .render (up_arrow ,True ,(100 ,200 ,255 ))
            self .screen .blit (up_surf ,(x_margin ,self .rect .y +self .history_start +30 ))

        if visible_end <len (move_history ):

            down_arrow ="▼ Scroll down"
            down_surf =self .font_small .render (down_arrow ,True ,(100 ,200 ,255 ))
            self .screen .blit (down_surf ,(x_margin ,self .rect .bottom -35 ))

        return y_offset 

    def draw_ai_thinking_overlay (self ):
        """
        Vẽ overlay khi AI đang suy nghĩ
        """

        overlay_height =60 
        overlay =pg .Surface ((self .rect .width -20 ,overlay_height ))
        overlay .set_alpha (200 )
        overlay .fill ((40 ,40 ,40 ))
        overlay_pos =(self .rect .x +10 ,self .rect .bottom -overlay_height -10 )
        self .screen .blit (overlay ,overlay_pos )


        overlay_rect =pg .Rect (overlay_pos [0 ],overlay_pos [1 ],
        self .rect .width -20 ,overlay_height )
        pg .draw .rect (self .screen ,(255 ,255 ,0 ),overlay_rect ,2 ,border_radius =5 )


        thinking_text =self .get_thinking_animation ()
        thinking_surf =self .font_medium .render (thinking_text ,True ,(255 ,255 ,0 ))
        thinking_rect =thinking_surf .get_rect (center =overlay_rect .center )
        self .screen .blit (thinking_surf ,thinking_rect )


        sub_text ="Calculating move..."
        sub_surf =self .font_small .render (sub_text ,True ,(200 ,200 ,200 ))
        sub_rect =sub_surf .get_rect (center =(overlay_rect .centerx ,
        overlay_rect .centery +20 ))
        self .screen .blit (sub_surf ,sub_rect )

    def get_thinking_animation (self ):
        """
        Tạo animation cho AI thinking
        
        Returns:
            str: Text với dots animation
        """
        dots =int (time .time ()*2 )%4 
        return "AI thinking"+"."*dots 

    def draw_game_over_overlay (self ,game_info ):
        """
        Vẽ overlay khi game kết thúc
        """

        overlay =pg .Surface ((self .rect .width ,self .rect .height ))
        overlay .set_alpha (230 )
        overlay .fill ((0 ,0 ,0 ))
        self .screen .blit (overlay ,(self .rect .x ,self .rect .y ))


        for i in range (3 ):
            glow_rect =pg .Rect (self .rect .x +i ,self .rect .y +i ,
            self .rect .width -2 *i ,self .rect .height -2 *i )
            pg .draw .rect (self .screen ,(255 ,215 ,0 ),glow_rect ,2 )

        y_center =self .rect .centery 


        title ="GAME OVER"
        title_surf =self .font_large .render (title ,True ,(255 ,215 ,0 ))
        title_rect =title_surf .get_rect (center =(self .rect .centerx ,y_center -80 ))
        self .screen .blit (title_surf ,title_rect )


        winner =game_info .get ('winner')
        if winner :
            result_text =f"{winner } WINS!"
            result_color =(100 ,255 ,100 )


            crown ="♔"
            crown_surf =self .font_large .render (crown ,True ,(255 ,215 ,0 ))
            crown_rect =crown_surf .get_rect (center =(self .rect .centerx ,y_center -30 ))
            self .screen .blit (crown_surf ,crown_rect )
        else :
            result_text ="DRAW!"
            result_color =(200 ,200 ,200 )

        result_surf =self .font_large .render (result_text ,True ,result_color )
        result_rect =result_surf .get_rect (center =(self .rect .centerx ,y_center +20 ))
        self .screen .blit (result_surf ,result_rect )


        instructions =[
        ("R","Restart"),
        ("ESC","Main Menu")
        ]

        y_offset =y_center +70 
        for key ,action in instructions :

            key_box =pg .Rect (self .rect .centerx -60 ,y_offset ,50 ,30 )
            pg .draw .rect (self .screen ,(60 ,60 ,60 ),key_box ,border_radius =3 )
            pg .draw .rect (self .screen ,UI_TEXT ,key_box ,2 ,border_radius =3 )

            key_surf =self .font_small .render (key ,True ,UI_TEXT )
            key_rect =key_surf .get_rect (center =key_box .center )
            self .screen .blit (key_surf ,key_rect )


            action_surf =self .font_small .render (action ,True ,(180 ,180 ,180 ))
            self .screen .blit (action_surf ,(self .rect .centerx ,y_offset +7 ))

            y_offset +=40 

    def draw_promotion_dialog (self ):
        """
        Vẽ dialog chọn quân phong cấp
        """

        overlay =pg .Surface ((self .rect .width ,self .rect .height ))
        overlay .set_alpha (220 )
        overlay .fill ((20 ,20 ,40 ))
        self .screen .blit (overlay ,(self .rect .x ,self .rect .y ))


        pg .draw .rect (self .screen ,(100 ,200 ,255 ),self .rect ,3 )


        title ="PAWN PROMOTION"
        title_surf =self .font_large .render (title ,True ,(100 ,200 ,255 ))
        title_rect =title_surf .get_rect (center =(self .rect .centerx ,
        self .rect .centery -100 ))
        self .screen .blit (title_surf ,title_rect )


        y_offset =self .rect .centery -50 
        options =[
        ("Q","Queen","♕",(255 ,215 ,0 )),
        ("R","Rook","♖",(200 ,200 ,200 )),
        ("B","Bishop","♗",(150 ,150 ,255 )),
        ("N","Knight","♘",(255 ,150 ,150 ))
        ]

        for key ,name ,icon ,color in options :

            option_box =pg .Rect (self .rect .x +30 ,y_offset ,
            self .rect .width -60 ,35 )
            pg .draw .rect (self .screen ,(40 ,40 ,60 ),option_box ,border_radius =5 )
            pg .draw .rect (self .screen ,color ,option_box ,2 ,border_radius =5 )


            icon_surf =self .font_medium .render (icon ,True ,color )
            icon_rect =icon_surf .get_rect (left =option_box .left +15 ,
            centery =option_box .centery )
            self .screen .blit (icon_surf ,icon_rect )


            key_text =f"[{key }]"
            key_surf =self .font_small .render (key_text ,True ,(150 ,150 ,150 ))
            key_rect =key_surf .get_rect (left =option_box .left +50 ,
            centery =option_box .centery )
            self .screen .blit (key_surf ,key_rect )


            name_surf =self .font_small .render (name ,True ,UI_TEXT )
            name_rect =name_surf .get_rect (left =option_box .left +100 ,
            centery =option_box .centery )
            self .screen .blit (name_surf ,name_rect )

            y_offset +=45 

    def handle_scroll (self ,direction ):
        """
        Xử lý scroll lịch sử nước đi
        
        Args:
            direction: 1 (scroll up) hoặc -1 (scroll down)
        """
        self .scroll_offset =max (0 ,self .scroll_offset +direction )

    def reset_scroll (self ):
        """Reset scroll về cuối (nước đi mới nhất)"""
        self .scroll_offset =0 

    def update_animation (self ,delta_time ):
        """
        Update animation (gọi mỗi frame)
        
        Args:
            delta_time: Thời gian delta giữa các frame
        """
        self .animation_time +=delta_time 

    def clear (self ):
        """Clear panel"""
        pg .draw .rect (self .screen ,UI_BACKGROUND ,self .rect )

    def draw_control_buttons (self ):
        """
        Vẽ các nút điều khiển (xoay bàn cờ, tua lùi)
        """

        button_width =80 
        button_height =30 
        button_spacing =10 


        rotate_x =self .rect .right -button_width -10 
        rotate_y =self .rect .bottom -button_height -10 

        rotate_rect =pg .Rect (rotate_x ,rotate_y ,button_width ,button_height )
        pg .draw .rect (self .screen ,(50 ,150 ,200 ),rotate_rect )
        pg .draw .rect (self .screen ,(255 ,255 ,255 ),rotate_rect ,2 )

        rotate_text =self .font_small .render ("ROTATE",True ,(255 ,255 ,255 ))
        rotate_text_rect =rotate_text .get_rect (center =rotate_rect .center )
        self .screen .blit (rotate_text ,rotate_text_rect )


        undo_x =rotate_x -button_width -button_spacing 
        undo_y =rotate_y 

        undo_rect =pg .Rect (undo_x ,undo_y ,button_width ,button_height )
        pg .draw .rect (self .screen ,(200 ,150 ,50 ),undo_rect )
        pg .draw .rect (self .screen ,(255 ,255 ,255 ),undo_rect ,2 )

        undo_text =self .font_small .render ("UNDO",True ,(255 ,255 ,255 ))
        undo_text_rect =undo_text .get_rect (center =undo_rect .center )
        self .screen .blit (undo_text ,undo_text_rect )

        return rotate_rect ,undo_rect 

    def is_rotate_button_clicked (self ,mouse_pos ):
        """
        Kiểm tra xem có click vào nút rotate không
        """
        button_width =80 
        button_height =30 
        button_x =self .rect .right -button_width -10 
        button_y =self .rect .bottom -button_height -10 

        button_rect =pg .Rect (button_x ,button_y ,button_width ,button_height )
        return button_rect .collidepoint (mouse_pos )

    def is_undo_button_clicked (self ,mouse_pos ):
        """
        Kiểm tra xem có click vào nút undo không
        """
        button_width =80 
        button_height =30 
        button_spacing =10 

        rotate_x =self .rect .right -button_width -10 
        undo_x =rotate_x -button_width -button_spacing 
        undo_y =self .rect .bottom -button_height -10 

        button_rect =pg .Rect (undo_x ,undo_y ,button_width ,button_height )
        return button_rect .collidepoint (mouse_pos )