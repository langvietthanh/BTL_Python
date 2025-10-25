

import random 

class OpeningBook :
    def __init__ (self ):
        """
        Khởi tạo opening book với các khai cuộc phổ biến
        """
        self .openings ={

        'italian':[
        {'from':[4 ,6 ],'to':[4 ,4 ]},
        {'from':[4 ,1 ],'to':[4 ,3 ]},
        {'from':[6 ,7 ],'to':[5 ,5 ]},
        {'from':[1 ,0 ],'to':[2 ,2 ]},
        {'from':[5 ,7 ],'to':[2 ,4 ]},
        ],


        'spanish':[
        {'from':[4 ,6 ],'to':[4 ,4 ]},
        {'from':[4 ,1 ],'to':[4 ,3 ]},
        {'from':[6 ,7 ],'to':[5 ,5 ]},
        {'from':[1 ,0 ],'to':[2 ,2 ]},
        {'from':[5 ,7 ],'to':[1 ,4 ]},
        ],


        'sicilian':[
        {'from':[4 ,6 ],'to':[4 ,4 ]},
        {'from':[2 ,1 ],'to':[2 ,3 ]},
        {'from':[6 ,7 ],'to':[5 ,5 ]},
        ],


        'french':[
        {'from':[4 ,6 ],'to':[4 ,4 ]},
        {'from':[4 ,1 ],'to':[4 ,2 ]},
        {'from':[3 ,6 ],'to':[3 ,4 ]},
        ],


        'queens_gambit':[
        {'from':[3 ,6 ],'to':[3 ,4 ]},
        {'from':[3 ,1 ],'to':[3 ,3 ]},
        {'from':[2 ,6 ],'to':[2 ,4 ]},
        ],


        'kings_indian':[
        {'from':[3 ,6 ],'to':[3 ,4 ]},
        {'from':[6 ,0 ],'to':[5 ,2 ]},
        {'from':[2 ,6 ],'to':[2 ,4 ]},
        {'from':[6 ,1 ],'to':[6 ,2 ]},
        ],
        }

    def get_opening_move (self ,move_history ):
        """
        Lấy nước đi từ opening book dựa trên lịch sử
        
        Args:
            move_history: List các Move đã đi
        
        Returns:
            dict: {'from': [x, y], 'to': [x, y]} hoặc None
        """
        if not move_history :

            first_moves =[
            {'from':[4 ,6 ],'to':[4 ,4 ]},
            {'from':[3 ,6 ],'to':[3 ,4 ]},
            ]
            return random .choice (first_moves )


        history_coords =[]
        for move in move_history :
            history_coords .append ({
            'from':[move .from_x ,move .from_y ],
            'to':[move .to_x ,move .to_y ]
            })


        matching_openings =[]
        for name ,opening_moves in self .openings .items ():

            if len (history_coords )<len (opening_moves ):
                matches =True 
                for i ,hist_move in enumerate (history_coords ):
                    if (hist_move ['from']!=opening_moves [i ]['from']or 
                    hist_move ['to']!=opening_moves [i ]['to']):
                        matches =False 
                        break 

                if matches :

                    next_move_index =len (history_coords )
                    matching_openings .append (opening_moves [next_move_index ])


        if matching_openings :
            return random .choice (matching_openings )

        return None 

    def add_opening (self ,name ,moves ):
        """
        Thêm một khai cuộc mới vào book
        
        Args:
            name: Tên khai cuộc
            moves: List các nước đi [{'from': [x,y], 'to': [x,y]}, ...]
        """
        self .openings [name ]=moves 