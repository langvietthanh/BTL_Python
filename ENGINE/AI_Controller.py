

from ENGINE .Minimax_AI import MinimaxAI 
from ENGINE .Opening_Book import OpeningBook 

class AIController :
    def __init__ (self ,difficulty ='medium',use_opening_book =True ):
        """
        Khởi tạo AI Controller
        
        Args:
            difficulty: 'easy', 'medium', 'hard'
            use_opening_book: Có dùng opening book không
        """
        self .ai =MinimaxAI (difficulty )
        self .use_opening_book =use_opening_book 
        self .opening_book =OpeningBook ()if use_opening_book else None 
        self .difficulty =difficulty 

    def get_ai_move (self ,board ,game_state ,color ):
        """
        Lấy nước đi từ AI
        
        Args:
            board: Chess_Board object
            game_state: GameState object
            color: 'White' hoặc 'Black'
        
        Returns:
            Move: Nước đi của AI
        """

        if self .use_opening_book and len (game_state .move_history )<10 :
            opening_move =self .opening_book .get_opening_move (game_state .move_history )
            if opening_move :

                from ENGINE .Move_Generator import MoveGenerator 
                move_gen =MoveGenerator (board )
                legal_moves =move_gen .generate_all_legal_moves (color ,game_state )

                for move in legal_moves :
                    if (move .from_x ==opening_move ['from'][0 ]and 
                    move .from_y ==opening_move ['from'][1 ]and 
                    move .to_x ==opening_move ['to'][0 ]and 
                    move .to_y ==opening_move ['to'][1 ]):
                        print (f"AI plays opening book move")
                        return move 


        print (f"AI thinking... (depth={self .ai .depth })")
        move =self .ai .find_best_move (board ,game_state ,color )
        return move 

    def set_difficulty (self ,difficulty ):
        """
        Thay đổi độ khó AI
        """
        self .difficulty =difficulty 
        self .ai .set_difficulty (difficulty )

    def toggle_opening_book (self ):
        """
        Bật/tắt opening book
        """
        self .use_opening_book =not self .use_opening_book 