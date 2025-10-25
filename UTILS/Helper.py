

from UTILS .Constants import *

def coordinate_to_notation (x ,y ):
    """
    Chuyển tọa độ (x, y) thành notation cờ vua (vd: e2)
    x: 0-7 (a-h)
    y: 0-7 (8-1)
    """
    if 0 <=x <=7 and 0 <=y <=7 :
        return FILES [x ]+RANKS [y ]
    return None 

def notation_to_coordinate (notation ):
    """
    Chuyển notation (vd: e2) thành tọa độ (x, y)
    """
    if len (notation )!=2 :
        return None 
    file =notation [0 ]
    rank =notation [1 ]
    if file in FILES and rank in RANKS :
        x =FILES .index (file )
        y =RANKS .index (rank )
        return [x ,y ]
    return None 

def is_valid_position (x ,y ):
    """
    Kiểm tra tọa độ có hợp lệ không (trong bàn cờ 8x8)
    """
    return 0 <=x <=7 and 0 <=y <=7 

def flip_coordinate_for_black (x ,y ):
    """
    Lật tọa độ cho quân đen (để dùng piece-square tables)
    """
    return x ,7 -y 

def move_to_notation (move ):
    """
    Chuyển đổi move object thành notation string
    vd: Move(e2 -> e4, Pawn) => "e4" hoặc "Nf3" (nếu là Knight)
    """
    if not move :
        return ""

    piece =move .piece .role 
    from_pos =coordinate_to_notation (move .from_x ,move .from_y )
    to_pos =coordinate_to_notation (move .to_x ,move .to_y )


    if piece =='pawn':
        if move .is_capture :
            return f"{FILES [move .from_x ]}x{to_pos }"
        return to_pos 


    piece_symbol ={
    'knight':'N',
    'bishop':'B',
    'rook':'R',
    'queen':'Q',
    'king':'K'
    }

    symbol =piece_symbol .get (piece ,'')
    capture ='x'if move .is_capture else ''

    notation =f"{symbol }{capture }{to_pos }"


    if move .is_checkmate :
        notation +='#'
    elif move .is_check :
        notation +='+'

    if move .is_castling :
        if move .to_x ==6 :
            notation ='O-O'
        else :
            notation ='O-O-O'

    if move .promotion_piece :
        notation +=f"={piece_symbol .get (move .promotion_piece ,'Q')}"

    return notation 

def get_opposite_color (color ):
    """
    Lấy màu đối diện
    """
    return 'Black'if color =='White'else 'White'

def count_material (board ):
    """
    Đếm giá trị vật chất trên bàn cờ
    Return: (white_value, black_value)
    """
    white_value =0 
    black_value =0 

    for piece in board .pieces :
        value =PIECE_VALUES .get (piece .role ,0 )
        if piece .color =='White':
            white_value +=value 
        else :
            black_value +=value 

    return white_value ,black_value 

def is_endgame (board ):
    """
    Kiểm tra xem có phải endgame không
    Endgame: không còn Queen hoặc tổng giá trị < 1300 cho mỗi bên
    """
    white_queens =sum (1 for p in board .pieces if p .role =='queen'and p .color =='White')
    black_queens =sum (1 for p in board .pieces if p .role =='queen'and p .color =='Black')


    if white_queens ==0 or black_queens ==0 :
        return True 


    white_value ,black_value =count_material (board )
    if white_value <1300 or black_value <1300 :
        return True 

    return False 

def format_time (seconds ):
    """
    Format thời gian từ giây sang MM:SS
    """
    minutes =int (seconds //60 )
    secs =int (seconds %60 )
    return f"{minutes :02d}:{secs :02d}"

def calculate_mobility (board ,color ):
    """
    Tính số nước đi có thể của một bên
    """
    from ENGINE .Move_Generator import MoveGenerator 
    move_gen =MoveGenerator (board )
    moves =move_gen .generate_all_moves (color )
    return len (moves )

def piece_symbol_unicode (piece ):
    """
    Lấy ký tự Unicode cho quân cờ (để hiển thị text)
    """
    symbols ={
    ('White','king'):'♔',
    ('White','queen'):'♕',
    ('White','rook'):'♖',
    ('White','bishop'):'♗',
    ('White','knight'):'♘',
    ('White','pawn'):'♙',
    ('Black','king'):'♚',
    ('Black','queen'):'♛',
    ('Black','rook'):'♜',
    ('Black','bishop'):'♝',
    ('Black','knight'):'♞',
    ('Black','pawn'):'♟',
    }
    return symbols .get ((piece .color ,piece .role ),'?')