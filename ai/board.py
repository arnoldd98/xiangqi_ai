import copy

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
COL = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
ROW = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
START_FEN = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'

'''
    Helper class for board, which contains the current state of the Xiangqi board and possible moves it can take
'''
class Board:
    def __init__(self, possible_moves, fen=None):
        self.board = self.fen_to_board(fen) if fen else self.fen_to_board(START_FEN)
        self.moves = possible_moves
        self.game_over = False
    
    def fen_to_board(self, fen):
        '''
            Convert a xiangqiFEN string to a 2D array of pieces
        '''
        board = [['.' for _ in range(9)] for _ in range(10)]
        rows = fen.split()[0].split('/')

        for row_idx, row in enumerate(rows):
            col_idx = 0
            for fen_piece in row:
                if fen_piece.isdigit():
                    col_idx += int(fen_piece)
                else:
                    board[row_idx][col_idx] = self._fen_to_piece(fen_piece)
                    col_idx += 1
        return board

    def get_moves(self):
        return self.moves
    
    def make_move(self, move):
        initial = move[0:2]
        final = move[2:4]
        initial_row_idx, initial_col_idx = self._get_idx_from_position(initial)
        final_row_idx, final_col_idx = self._get_idx_from_position(final)

        self.prev_board = copy.deepcopy(self.board)
        piece = self.get_piece(initial)
        self.board[initial_row_idx][initial_col_idx] = '.'
        self.board[final_row_idx][final_col_idx] = piece

    def undo(self):
        self.board = copy.deepcopy(self.prev_board)

    def get_piece(self, position):
        row_idx, col_idx = self._get_idx_from_position(position)
        return self.board[row_idx][col_idx]

    def _get_idx_from_position(self, position):
        row_idx = int(position[1])
        col_idx = COL.get(position[0])
        return row_idx, col_idx

    def _fen_to_piece(self, fen_piece):
        if fen_piece.islower():
            return 'b' + fen_piece.upper()
        else:
            return 'r' + fen_piece.upper()
    
        

