'''
    Notations:
        - .: empty
        - b: black
        - r: red
        - R: che
        - N: 马
        - B: 象
        - A: 士
        - K: 将
        - C: 炮
        - P: 兵
'''

ROW_LENGTH = 10
COL_LENGTH = 9
START_FEN = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'

'''
    Helper class for board, which contains the current state of the Xiangqi board and possible moves it can take
'''
class Board:
    def __init__(self, possible_moves, fen=None):
        self.board = self.fen_to_board(fen) if fen else self.fen_to_board(START_FEN)
    
    def fen_to_board(self, fen):
        '''
            Convert a xiangqiFEN string to a 2D array of pieces
        '''
        board = [[None for _ in range(9)] for _ in range(10)]
        rows = fen.split()[0].split('/')

        for row_idx, row in enumerate(rows):
            col_idx = 0
            for fen_piece in row:
                if fen_piece.isdigit():
                    board[row_idx][col_idx] = '.'
                    col_idx += int(fen_piece)
                else:
                    board[row_idx][col_idx] = self._fen_to_piece(fen_piece)
                    col_idx += 1
        return board
    
    def _fen_to_piece(self, fen_piece):
        if fen_piece.islower():
            return 'b' + fen_piece.upper()
        else:
            return 'r' + fen_piece.upper()
        

