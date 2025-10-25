import pygame as pg
from pygame .locals import *
import sys 


from MODEL .Chess_Board import Board 
from MODEL .Game_State import GameState 


from VIEW .Board_View import Board_View 
from VIEW .Menu_View import MenuView 
from VIEW .Info_Panel import InfoPanel 


from CONTROLLER .Game_Controller import GameController 


from UTILS .Constants import *

def main ():
    pg .init ()
    pg .display .set_caption ("Chess AI - Python Project")
    screen =pg .display .set_mode ((WINDOW_WIDTH ,WINDOW_HEIGHT ))
    clock =pg .time .Clock ()
    game_started =False 
    in_menu =True 
    menu_view =MenuView (screen )
    board =None 
    board_view =None 
    game_controller =None 
    info_panel =None 
    running =True 
    while running :
        for event in pg .event .get ():
            if event .type ==QUIT :
                running =False 
            elif event .type ==KEYDOWN :
                if event .key ==K_ESCAPE :
                    if game_started and game_controller and not game_controller .game_state .game_over :
                        in_menu =True 
                        game_started =False 
                        menu_view .reset ()
                elif event .key ==K_r and game_started and game_controller and not game_controller .game_state .game_over :
                    game_controller .reset_game ()
            if in_menu :
                action =menu_view .handle_event (event )
                if action =='quit':
                    running =False 
                elif action =='start_game':
                    settings =menu_view .get_game_settings ()
                    board =Board ()
                    board_view =Board_View (screen ,board )
                    board_view .init_piece ()
                    game_controller =GameController (
                    board ,
                    board_view ,
                    game_mode =settings ['mode'],
                    ai_difficulty =settings ['difficulty']
                    )
                    if settings ['mode']=='PVE':
                        game_controller .ai_color =settings ['ai_color']
                        if settings ['ai_color']=='White':
                            game_controller .ai_thinking =True 
                    info_panel =InfoPanel (
                    screen ,
                    BOARD_SIZE *CELL_SIZE +10 ,
                    0 ,
                    INFO_PANEL_WIDTH -20 ,
                    WINDOW_HEIGHT 
                    )
                    in_menu =False 
                    game_started =True 
                    print (f"Game started: {settings ['mode']}, Difficulty: {settings ['difficulty']}")
            elif game_started and game_controller :
                if game_controller .game_state .game_over :
                    if event .type ==KEYDOWN :
                        if event .key ==K_r :
                            game_controller .reset_game ()
                            print ("Game restarted!")
                        elif event .key ==K_ESCAPE :
                            in_menu =True 
                            game_started =False 
                            game_controller =None 
                            board_view =None 
                            info_panel =None 
                            menu_view .reset ()
                            print ("Returned to menu")
                elif game_controller .waiting_for_promotion :
                    game_controller .handle_promotion_choice (event )
                else :
                    game_controller .handle_events (event )
                    if event .type ==pg .MOUSEBUTTONDOWN and info_panel :
                        if info_panel .is_rotate_button_clicked (event .pos ):
                            board_view .toggle_board_rotation ()
                            print ("Board rotated")
                        elif info_panel .is_undo_button_clicked (event .pos ):
                            if game_controller .undo_move ():
                                print ("Move undone")
                            else :
                                print ("No moves to undo")
        if game_started and game_controller :
            if game_controller .ai_thinking and not game_controller .game_state .game_over :
                game_controller .update_ai ()
            if game_controller .selected_piece :
                board_view .set_valid_moves (game_controller .valid_moves )
            else :
                board_view .set_valid_moves ([])
            if game_controller .game_state .move_history :
                board_view .set_last_move (game_controller .game_state .move_history [-1 ])
        screen .fill ((0 ,0 ,0 ))
        if in_menu :
            menu_view .draw ()
        elif game_started :
            board_view .draw_board ()
            if game_controller and game_controller .waiting_for_promotion :
                game_controller .draw_promotion_selection (screen )
            if info_panel and game_controller :
                game_info =game_controller .get_game_info ()
                info_panel .draw (game_info ,game_controller .game_state .move_history )
                if game_info ['game_over']:
                    info_panel .draw_game_over_overlay (game_info )
            pg .display .flip ()
        clock .tick (FPS )
    pg .quit ()
    sys .exit ()


if __name__ =="__main__":
    main ()
