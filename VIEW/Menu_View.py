

import pygame as pg 
from UTILS .Constants import *

class Button :
    def __init__ (self ,x ,y ,width ,height ,text ,font_size =FONT_MEDIUM ):
        self .rect =pg .Rect (x ,y ,width ,height )
        self .text =text 
        self .font =pg .font .Font (None ,font_size )
        self .is_hovered =False 
        self .is_active =False 

    def draw (self ,screen ):

        if self .is_active :
            color =UI_BUTTON_ACTIVE 
        elif self .is_hovered :
            color =UI_BUTTON_HOVER 
        else :
            color =UI_BUTTON 


        pg .draw .rect (screen ,color ,self .rect )
        pg .draw .rect (screen ,UI_TEXT ,self .rect ,2 )


        text_surf =self .font .render (self .text ,True ,UI_TEXT )
        text_rect =text_surf .get_rect (center =self .rect .center )
        screen .blit (text_surf ,text_rect )

    def check_hover (self ,mouse_pos ):
        self .is_hovered =self .rect .collidepoint (mouse_pos )
        return self .is_hovered 

    def is_clicked (self ,mouse_pos ):
        return self .rect .collidepoint (mouse_pos )


class MenuView :
    def __init__ (self ,screen ):
        self .screen =screen 
        self .font_large =pg .font .Font (None ,FONT_LARGE )
        self .font_medium =pg .font .Font (None ,FONT_MEDIUM )
        self .font_small =pg .font .Font (None ,FONT_SMALL )


        self .current_menu ='main'
        self .selected_mode =None 
        self .selected_difficulty =None 
        self .selected_ai_color =None 


        self .setup_buttons ()

    def setup_buttons (self ):
        """Tạo các nút bấm"""
        center_x =WINDOW_WIDTH //2 
        button_width =300 
        button_height =60 
        button_spacing =80 
        start_y =250 


        self .main_buttons ={
        'play':Button (center_x -button_width //2 ,start_y ,
        button_width ,button_height ,"PLAY NOW"),
        'quit':Button (center_x -button_width //2 ,start_y +button_spacing ,
        button_width ,button_height ,"QUIT")
        }


        self .mode_buttons ={
        'PVP':Button (center_x -button_width //2 ,start_y ,
        button_width ,button_height ,"PLAYER vs PLAYER"),
        'PVE':Button (center_x -button_width //2 ,start_y +button_spacing ,
        button_width ,button_height ,"PLAYER vs AI"),
        'back':Button (center_x -button_width //2 ,start_y +button_spacing *2 ,
        button_width ,button_height ,"BACK")
        }


        self .difficulty_buttons ={
        'easy':Button (center_x -button_width //2 ,start_y ,
        button_width ,button_height ,"EASY"),
        'medium':Button (center_x -button_width //2 ,start_y +button_spacing ,
        button_width ,button_height ,"MEDIUM"),
        'hard':Button (center_x -button_width //2 ,start_y +button_spacing *2 ,
        button_width ,button_height ,"HARD"),
        'back':Button (center_x -button_width //2 ,start_y +button_spacing *3 ,
        button_width ,button_height ,"BACK")
        }


        self .color_buttons ={
        'white':Button (center_x -button_width //2 ,start_y ,
        button_width ,button_height ,"PLAY AS WHITE"),
        'black':Button (center_x -button_width //2 ,start_y +button_spacing ,
        button_width ,button_height ,"PLAY AS BLACK"),
        'back':Button (center_x -button_width //2 ,start_y +button_spacing *2 ,
        button_width ,button_height ,"BACK")
        }

    def draw (self ):
        """Vẽ menu"""
        self .screen .fill (UI_BACKGROUND )


        title =self .font_large .render ("CHESS AI",True ,UI_TEXT )
        title_rect =title .get_rect (center =(WINDOW_WIDTH //2 ,150 ))
        self .screen .blit (title ,title_rect )


        if self .current_menu =='main':
            self .draw_main_menu ()
        elif self .current_menu =='mode_select':
            self .draw_mode_menu ()
        elif self .current_menu =='difficulty_select':
            self .draw_difficulty_menu ()
        elif self .current_menu =='color_select':
            self .draw_color_menu ()

        pg .display .flip ()

    def draw_main_menu (self ):
        """Vẽ main menu"""
        for button in self .main_buttons .values ():
            button .draw (self .screen )


        credits =self .font_small .render ("Python Project - Chess AI",True ,UI_TEXT )
        credits_rect =credits .get_rect (center =(WINDOW_WIDTH //2 ,WINDOW_HEIGHT -50 ))
        self .screen .blit (credits ,credits_rect )

    def draw_mode_menu (self ):
        """Vẽ menu chọn chế độ"""
        subtitle =self .font_medium .render ("SELECT GAME MODE",True ,UI_TEXT )
        subtitle_rect =subtitle .get_rect (center =(WINDOW_WIDTH //2 ,200 ))
        self .screen .blit (subtitle ,subtitle_rect )

        for button in self .mode_buttons .values ():
            button .draw (self .screen )

    def draw_difficulty_menu (self ):
        """Vẽ menu chọn độ khó"""
        subtitle =self .font_medium .render ("SELECT DIFFICULTY",True ,UI_TEXT )
        subtitle_rect =subtitle .get_rect (center =(WINDOW_WIDTH //2 ,200 ))
        self .screen .blit (subtitle ,subtitle_rect )

        for button in self .difficulty_buttons .values ():
            button .draw (self .screen )

    def draw_color_menu (self ):
        """Vẽ menu chọn màu quân"""
        subtitle =self .font_medium .render ("SELECT PIECE COLOR",True ,UI_TEXT )
        subtitle_rect =subtitle .get_rect (center =(WINDOW_WIDTH //2 ,200 ))
        self .screen .blit (subtitle ,subtitle_rect )

        for button in self .color_buttons .values ():
            button .draw (self .screen )

    def handle_event (self ,event ):
        """
        Xử lý sự kiện menu
        
        Returns:
            str hoặc None: Action cần thực hiện ('start_game', 'quit', None)
        """
        if event .type ==pg .MOUSEMOTION :
            mouse_pos =event .pos 

            if self .current_menu =='main':
                for button in self .main_buttons .values ():
                    button .check_hover (mouse_pos )
            elif self .current_menu =='mode_select':
                for button in self .mode_buttons .values ():
                    button .check_hover (mouse_pos )
            elif self .current_menu =='difficulty_select':
                for button in self .difficulty_buttons .values ():
                    button .check_hover (mouse_pos )
            elif self .current_menu =='color_select':
                for button in self .color_buttons .values ():
                    button .check_hover (mouse_pos )

        elif event .type ==pg .MOUSEBUTTONDOWN :
            mouse_pos =event .pos 
            return self .handle_click (mouse_pos )

        return None 

    def handle_click (self ,mouse_pos ):
        """Xử lý click chuột"""
        if self .current_menu =='main':
            if self .main_buttons ['play'].is_clicked (mouse_pos ):
                self .current_menu ='mode_select'
            elif self .main_buttons ['quit'].is_clicked (mouse_pos ):
                return 'quit'

        elif self .current_menu =='mode_select':
            if self .mode_buttons ['PVP'].is_clicked (mouse_pos ):
                self .selected_mode ='PVP'
                return 'start_game'
            elif self .mode_buttons ['PVE'].is_clicked (mouse_pos ):
                self .selected_mode ='PVE'
                self .current_menu ='color_select'
            elif self .mode_buttons ['back'].is_clicked (mouse_pos ):
                self .current_menu ='main'

        elif self .current_menu =='color_select':
            if self .color_buttons ['white'].is_clicked (mouse_pos ):
                self .selected_ai_color ='Black'
                self .current_menu ='difficulty_select'
            elif self .color_buttons ['black'].is_clicked (mouse_pos ):
                self .selected_ai_color ='White'
                self .current_menu ='difficulty_select'
            elif self .color_buttons ['back'].is_clicked (mouse_pos ):
                self .current_menu ='mode_select'

        elif self .current_menu =='difficulty_select':
            if self .difficulty_buttons ['easy'].is_clicked (mouse_pos ):
                self .selected_difficulty ='easy'
                return 'start_game'
            elif self .difficulty_buttons ['medium'].is_clicked (mouse_pos ):
                self .selected_difficulty ='medium'
                return 'start_game'
            elif self .difficulty_buttons ['hard'].is_clicked (mouse_pos ):
                self .selected_difficulty ='hard'
                return 'start_game'
            elif self .difficulty_buttons ['back'].is_clicked (mouse_pos ):
                if self .selected_mode =='PVE':
                    self .current_menu ='color_select'
                else :
                    self .current_menu ='mode_select'

        return None 

    def get_game_settings (self ):
        """
        Lấy cài đặt game đã chọn
        """
        return {
        'mode':self .selected_mode or 'PVP',
        'difficulty':self .selected_difficulty or 'medium',
        'ai_color':self .selected_ai_color or 'Black'
        }

    def reset (self ):
        """Reset menu về trạng thái ban đầu"""
        self .current_menu ='main'
        self .selected_mode =None 
        self .selected_difficulty =None 
        self .selected_ai_color =None 