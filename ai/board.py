from cmath import pi
import copy
from copy import deepcopy
from prettyprinter import pprint
from collections import deque

'''
    Notations:
        - .: empty
        - b: black
        - r: red
        - R: che
        - N: 马, horse
        - B: 象, elephant
        - A: 士, advisor
        - K: 将, general
        - C: 炮, cannon
        - P: 兵, pawn

    Board:
        a9 b9 c9 d9 e9 f9 g9 h9 i9
        a8 b8 c8 d8 e8 f8 g8 h8 i8
        a7 b7 c7 d7 e7 f7 g7 h7 i7
        a6 b6 c6 d6 e6 f6 g6 h6 i6
        a5 b5 c5 d5 e5 f5 g5 h5 i5
        a4 b4 c4 d4 e4 f4 g4 h4 i4
        a3 b3 c3 d3 e3 f3 g3 h3 i3
        a2 b2 c2 d2 e2 f2 g2 h2 i2
        a1 b1 c1 d1 e1 f1 g1 h1 i1
        a0 b0 c0 d0 e0 f0 g0 h0 i0

    Board position represented by either
    - idx: (col (x), row (y)). To get board position from idx, use board[idx[1]][idx[0]]
    - notation: col+row

'''

# declare constants
ROW_LENGTH = 10
COL_LENGTH = 9
COL = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
COL_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
ROW = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
START_FEN = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'

BOARD_POSITIONS = [
    ['a9', 'b9', 'c9', 'd9', 'e9', 'f9', 'g9', 'h9', 'i9'],
    ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8', 'i8'],
    ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'i7'],
    ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6', 'i6'],
    ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5', 'i5'],
    ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4', 'i4'],
    ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3', 'i3'],
    ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 'i2'],
    ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'i1'],
    ['a0', 'b0', 'c0', 'd0', 'e0', 'f0', 'g0', 'h0', 'i0']
]

BOARD_POSITIONS_DICT = {
    'a9': (0, 0), 'b9': (1, 0), 'c9': (2, 0), 'd9': (3, 0), 'e9': (4, 0), 'f9': (5, 0), 'g9': (6, 0), 'h9': (7, 0), 'i9': (8, 0),
    'a8': (0, 1), 'b8': (1, 1), 'c8': (2, 1), 'd8': (3, 1), 'e8': (4, 1), 'f8': (5, 1), 'g8': (6, 1), 'h8': (7, 1), 'i8': (8, 1),
    'a7': (0, 2), 'b7': (1, 2), 'c7': (2, 2), 'd7': (3, 2), 'e7': (4, 2), 'f7': (5, 2), 'g7': (6, 2), 'h7': (7, 2), 'i7': (8, 2),
    'a6': (0, 3), 'b6': (1, 3), 'c6': (2, 3), 'd6': (3, 3), 'e6': (4, 3), 'f6': (5, 3), 'g6': (6, 3), 'h6': (7, 3), 'i6': (8, 3),
    'a5': (0, 4), 'b5': (1, 4), 'c5': (2, 4), 'd5': (3, 4), 'e5': (4, 4), 'f5': (5, 4), 'g5': (6, 4), 'h5': (7, 4), 'i5': (8, 4),
    'a4': (0, 5), 'b4': (1, 5), 'c4': (2, 5), 'd4': (3, 5), 'e4': (4, 5), 'f4': (5, 5), 'g4': (6, 5), 'h4': (7, 5), 'i4': (8, 5),
    'a3': (0, 6), 'b3': (1, 6), 'c3': (2, 6), 'd3': (3, 6), 'e3': (4, 6), 'f3': (5, 6), 'g3': (6, 6), 'h3': (7, 6), 'i3': (8, 6),
    'a2': (0, 7), 'b2': (1, 7), 'c2': (2, 7), 'd2': (3, 7), 'e2': (4, 7), 'f2': (5, 7), 'g2': (6, 7), 'h2': (7, 7), 'i2': (8, 7),
    'a1': (0, 8), 'b1': (1, 8), 'c1': (2, 8), 'd1': (3, 8), 'e1': (4, 8), 'f1': (5, 8), 'g1': (6, 8), 'h1': (7, 8), 'i1': (8, 8),
    'a0': (0, 9), 'b0': (1, 9), 'c0': (2, 9), 'd0': (3, 9), 'e0': (4, 9), 'f0': (5, 9), 'g0': (6, 9), 'h0': (7, 9), 'i0': (8, 9)
}



'''
    Helper class for board, which contains the current state of the Xiangqi board and possible moves it can take
'''
class Board:
    def __init__(self, fen=None, current_side='b'):
        self.board = self.fen_to_board(fen) if fen else self.fen_to_board(START_FEN)
        self.start = True
        self.side = current_side
        self.check = '.'
        self.history = deque()

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

    def set_side(self, side):
        self.side = side

    def get_moves(self):
        # if self.start and not self.moves == None:
        #     self.start = False
        #     return self.moves
        
        return self.generate_moves(self.side)
        
    def make_move(self, move, change_side=False):
        initial = move[0:2]
        final = move[2:4]
        initial_col_idx, initial_row_idx = self._get_idx_from_position(initial)
        final_col_idx, final_row_idx = self._get_idx_from_position(final)

        # save board state (before making move) to history
        self.history.append(copy.deepcopy(self.board))

        # modify current board
        piece = self.get_piece(position=initial)
        self.board[initial_row_idx][initial_col_idx] = '.'
        self.board[final_row_idx][final_col_idx] = piece
        if change_side:
            self.change_side()

    def undo(self, change_side=False):
        if len(self.history) == 0:
            return

        self.board = self.history.pop()
        if change_side:
            self.change_side()
    
    def change_side(self):
        self.side = 'r' if self.side == 'b' else 'b'

    def get_piece(self, position = '', col_idx=-1, row_idx=-1):
        if row_idx != -1 and col_idx != -1:
            return self.board[row_idx][col_idx]
        col_idx, row_idx = self._get_idx_from_position(position)
        return self.board[row_idx][col_idx]
    
    def get_position(self, piece):
        position_idxes = self.get_position_idx(piece)
        return [self._get_position_from_idx(i) for i in position_idxes]
    
    def get_position_idx(self, piece):
        positions = []
        for row_idx, row in enumerate(self.board):
            for col_idx, piece_ in enumerate(row):
                if piece_ == piece:
                    positions.append((col_idx, row_idx))
        return positions

    def generate_moves(self, side):
        '''
            Generate all possible moves for the current board
        '''
        legal_moves = []
        for row_idx, row in enumerate(self.board):
            for col_idx, piece in enumerate(row):
                if piece[0] != side:
                    continue
                side = piece[0]
                position_idx = (col_idx, row_idx)
                if piece[1] == 'K':
                    legal_moves.extend(self._generate_king_moves(position_idx, side))
                elif piece[1] == 'A':
                    legal_moves.extend(self._generate_advisor_moves(position_idx, side))
                elif piece[1] == 'R':
                    legal_moves.extend(self._generate_rook_moves(position_idx, side))
                elif piece[1] == 'C':
                    legal_moves.extend(self._generate_cannon_moves(position_idx, side))
                elif piece[1] == 'B':
                    legal_moves.extend(self._generate_elephant_moves(position_idx, side))
                elif piece[1] == 'P':
                    legal_moves.extend(self._generate_pawn_moves(position_idx, side))
                elif piece[1] == 'N':
                    legal_moves.extend(self._generate_horse_moves(position_idx, side))
        
        # legal_moves_copy = deepcopy(legal_moves)
        # if self.is_check(side):
        #     for move in legal_moves_copy:
        #         self.make_move(move, change_side=False)
        #         if self.is_check(side):
        #             legal_moves.remove(move)
        #         self.undo()
        # else:
        legal_moves_copy = deepcopy(legal_moves)
        for move in legal_moves_copy:
            self.make_move(move, change_side=False)
            if self.is_check(side):
                legal_moves.remove(move)
            self.undo()

        self.moves = legal_moves
        
        return legal_moves
    
    def is_checkmate(self):
        moves = self.generate_moves(self.side)
        return len(moves) == 0
    
    def is_check(self, side):
        '''
            Check if the given side is in check
        '''
        if len(self.get_position_idx(side + 'K')) == 0:
            print('ERROR: NO KING WTF')
            print('Side: ', side)
            pprint(self.board)

        general_position_idx = self.get_position_idx(side + 'K')[0]
        g_pos_idx_x, g_pos_idx_y = general_position_idx
        opp = 'r' if side == 'b' else 'b'
        
        # check for horse
        for offsets in [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]:
            horse_x_idx = g_pos_idx_x + offsets[0]
            horse_y_idx = g_pos_idx_y + offsets[1]
            if self._check_out_of_board(horse_x_idx, horse_y_idx):
                continue

            if self.get_piece(row_idx=horse_y_idx, col_idx=horse_x_idx) == opp + 'N':
                if self._hobbling_horse_leg(horse_pos_idx=(horse_x_idx, horse_y_idx), final_pos_idx=general_position_idx):
                    continue
                return True
        
        # check for cannon, rook, general
        for direction in [-1, 1]:   # check for horizontal
            skipped = False
            check_x = g_pos_idx_x + direction
            while check_x >= 0 and check_x < COL_LENGTH-1:
                piece = self.get_piece(row_idx=g_pos_idx_y, col_idx=check_x)
                if self._check_out_of_board(check_x, g_pos_idx_y):
                    break
                if skipped:
                    if piece == opp + 'C':
                        return True
                    if piece != '.':
                        break
                elif piece == opp + 'R' or piece == opp + 'G':
                    return True
                elif piece != '.':
                    skipped = True
                check_x += direction
        
        for direction in [-1, 1]:   # check for vertical
            skipped = False
            check_y = g_pos_idx_y + direction
            while check_y >= 0 and check_y < ROW_LENGTH-1:
                piece = self.get_piece(row_idx=check_y, col_idx=g_pos_idx_x)
                if self._check_out_of_board(g_pos_idx_x, check_y):
                    break
                if skipped:
                    if piece == opp + 'C':
                        return True
                    if piece != '.':
                        break
                elif piece == opp + 'R' or piece == opp + 'G':
                    return True
                elif piece != '.':
                    skipped = True
                check_y += direction
                
        # check for pawn
        for offsets in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            pawn_x_idx = g_pos_idx_x + offsets[0]
            pawn_y_idx = g_pos_idx_y + offsets[1]
            if self._check_out_of_board(pawn_x_idx, pawn_y_idx):
                continue
            if self.get_piece(row_idx=pawn_y_idx, col_idx=pawn_x_idx) == opp + 'P':
                return True
        return False

    def _get_idx_from_position(self, position):
        # for row_idx, row in enumerate(BOARD_POSITIONS):
        #     for col_idx, piece in enumerate(row):
        #         if piece == position:
        #             return col_idx, row_idx
        # return None
        return BOARD_POSITIONS_DICT[position]
    
    def _get_position_from_idx(self, position_idx):
        col_idx, row_idx = position_idx
        return BOARD_POSITIONS[row_idx][col_idx]

    def _fen_to_piece(self, fen_piece):
        if fen_piece.islower(): 
            return 'b' + fen_piece.upper()
        else:
            return 'r' + fen_piece.upper()
    
    def _check_out_of_board(self, col_idx, row_idx):
        return row_idx < 0 or row_idx >= ROW_LENGTH or col_idx <  0 or col_idx >= COL_LENGTH
    
    def _hobbling_horse_leg(self, horse_pos=None, final_pos=None, horse_pos_idx=(-1,-1), final_pos_idx=(-1,-1)):
        if horse_pos != None and final_pos != None:
            col_idx, row_idx = self._get_idx_from_position(horse_pos)
            final_col_idx, final_row_idx = self._get_idx_from_position(final_pos)
        elif horse_pos_idx != (-1,-1) and final_pos_idx != (-1,-1):
            col_idx, row_idx = horse_pos_idx
            final_col_idx, final_row_idx = final_pos_idx

        action = (final_col_idx - col_idx, final_row_idx - row_idx)

        if action == (2, 1) or action == (2, -1):
            blocker_idx = (col_idx + 1, row_idx)
        elif action == (-2, 1) or action == (-2, -1):
            blocker_idx = (col_idx - 1, row_idx)
        elif action == (1, 2) or action == (-1, 2):
            blocker_idx = (col_idx, row_idx + 1)
        elif action == (1, -2) or action == (-1, -2):
            blocker_idx = (col_idx, row_idx - 1)
        else:
            raise Exception('Invalid horse action')
        return self.board[blocker_idx[1]][blocker_idx[0]] != '.'
            

    def _generate_king_moves(self, position_idx, side):
        moves = []
        opp = 'r' if side == 'b' else 'b'
        if side == 'r':
            legal_positions = ['d2', 'e2', 'f2', 'd1', 'e1', 'f1', 'd0', 'e0', 'f0']
        elif side == 'b':
            legal_positions = ['d7', 'e7', 'f7', 'd8', 'e8', 'f8', 'd9', 'e9', 'f9']
        col_idx, row_idx = position_idx
        for action in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row_idx = row_idx + action[0]
            new_col_idx = col_idx + action[1]
            if self._check_out_of_board(new_col_idx, new_row_idx):
                continue
            new_board_slot = self.board[new_row_idx][new_col_idx]
            new_pos = self._get_position_from_idx((new_col_idx, new_row_idx))
            if new_board_slot == '.' or new_board_slot[0] == opp:
                if new_pos in legal_positions:
                    # check for flying general
                    front_idx = new_col_idx
                    opp_general = opp + 'K'
                    invalid = True
                    if side == 'r':
                        while self.board[new_row_idx][front_idx] != opp_general:
                            front_idx += 1
                            if front_idx == 9 or self.board[new_row_idx][front_idx] != '.':
                                invalid = False
                                break
                            
                    elif side == 'b':
                        while self.board[new_row_idx][front_idx] != opp_general:
                            front_idx -= 1
                            if front_idx == 0 or self.board[new_row_idx][front_idx] != '.':
                                invalid = False
                                break

                    if not invalid:
                        move = self._get_position_from_idx(position_idx) + new_pos
                        moves.append(move) 
        return moves

    def _generate_advisor_moves(self, position_idx, side):
        moves = []
        opp = 'r' if side == 'b' else 'b'
        if side == 'r':
            legal_positions = ['d0', 'f0', 'e1', 'd2', 'f2']
        elif side == 'b':
            legal_positions = ['d9', 'f9', 'e8', 'd7', 'f7']
        col_idx, row_idx = position_idx
        for action in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            new_row_idx = row_idx + action[1]
            new_col_idx = col_idx + action[0]
            if self._check_out_of_board(new_col_idx, new_row_idx):
                continue
            new_pos = self.board[new_row_idx][new_col_idx]
            if new_pos == '.' or new_pos[0] == opp:
                new_position = self._get_position_from_idx((new_col_idx, new_row_idx))
                if new_position in legal_positions:
                    move = self._get_position_from_idx(position_idx) + new_position
                    moves.append(move)
        return moves
    
    def _generate_rook_moves(self, position_idx, side):
        moves = []
        position = self._get_position_from_idx(position_idx)
        col_idx, row_idx = position_idx
        opp = 'r' if side == 'b' else 'b'
        
        # check for horizontal moves
        for direction in [-1, 1]:
            limit_x = col_idx
            while (limit_x > 0 and direction == -1) or (limit_x < COL_LENGTH-1 and direction  == 1):
                limit_x += direction
                new_pos = self.board[row_idx][limit_x]
                if new_pos == '.':
                    moves.append(position + self._get_position_from_idx((limit_x, row_idx)))
                elif new_pos[0] == opp:
                    moves.append(position + self._get_position_from_idx((limit_x, row_idx)))
                    break
                elif new_pos[0] == side:
                    break

        # check for vertical moves
        for direction in [-1, 1]:
            limit_y = row_idx
            while (limit_y > 0 and direction == -1) or (limit_y < ROW_LENGTH-1 and direction == 1):
                limit_y += direction
                new_pos = self.board[limit_y][col_idx]
                if new_pos == '.':
                    moves.append(position + self._get_position_from_idx((col_idx, limit_y)))
                elif new_pos[0] == opp:
                    moves.append(position + self._get_position_from_idx((col_idx, limit_y)))
                    break
                elif new_pos[0] == side:
                    break
        return moves

    def _generate_cannon_moves(self, position_idx, side):
        moves = []
        position = self._get_position_from_idx(position_idx)
        col_idx, row_idx = position_idx
        opp = 'r' if side == 'b' else 'b'

        # check for horizontal moves
        for direction in [-1, 1]:
            limit_x = col_idx
            skipped = False
            while limit_x > 0 and limit_x < COL_LENGTH-1:
                limit_x += direction
                new_pos = self.board[row_idx][limit_x]
                if new_pos == '.' and not skipped:
                    moves.append(position + self._get_position_from_idx((limit_x, row_idx)))
                elif new_pos != '.' and not skipped:
                    skipped = True
                elif new_pos[0] == opp and skipped:
                    moves.append(position + self._get_position_from_idx((limit_x, row_idx)))
                    break
                elif new_pos[0] == side and skipped:
                    break
        
        # check for vertical moves
        for direction in [-1, 1]:
            limit_y = row_idx
            skipped = False
            while limit_y > 0 and limit_y < ROW_LENGTH-1:
                limit_y += direction
                new_pos = self.board[limit_y][col_idx]
                if new_pos == '.' and not skipped:
                    moves.append(position + self._get_position_from_idx((col_idx, limit_y)))
                elif new_pos != '.' and not skipped:
                    skipped = True
                elif new_pos[0] == opp and skipped:
                    moves.append(position + self._get_position_from_idx((col_idx, limit_y)))
                    break
                elif new_pos[0] == side and skipped:
                    break
        return moves
    
    def _generate_elephant_moves(self, position_idx, side):
        moves = []
        opp = 'r' if side == 'b' else 'b'
        if side == 'r':
            legal_positions = ['c0', 'g0', 'a2', 'e2', 'i2', 'c4', 'g4']
        elif side == 'b':
            legal_positions = ['c9', 'g9', 'a7', 'e7', 'i7', 'c5', 'g5']
        col_idx, row_idx = position_idx
        for action in [(2, 2), (2, -2), (-2, 2), (-2, -2)]:
            new_row_idx = row_idx + action[0]
            new_col_idx = col_idx + action[1]
            if self._check_out_of_board(new_col_idx, new_row_idx):
                continue
            
            # check if elephant is blocked
            block_row_idx = int(row_idx + action[0]/2)
            block_col_idx = int(col_idx + action[1]/2)
            if self.board[block_row_idx][block_col_idx] != '.':
                continue

            new_pos = self.board[new_row_idx][new_col_idx]
            if new_pos == '.' or new_pos[0] == opp:
                new_position = self._get_position_from_idx((new_col_idx, new_row_idx))
                if new_position in legal_positions:
                    move = self._get_position_from_idx(position_idx) + new_position
                    moves.append(move)

        return moves
    
    def _generate_pawn_moves(self, position_idx, side):
        moves = []
        opp = 'r' if side == 'b' else 'b'
        col_idx, row_idx = position_idx
        position = self._get_position_from_idx(position_idx)

        if side == 'b':
            if row_idx < 9:
                if self.board[row_idx+1][col_idx][0] != side:
                    moves.append(position + self._get_position_from_idx((col_idx, row_idx + 1)))
            if row_idx >= 5:
                if col_idx < 8:
                    if self.board[row_idx][col_idx+1][0] != side:
                        moves.append(position + self._get_position_from_idx((col_idx + 1, row_idx)))
                if col_idx > 0:
                    if self.board[row_idx][col_idx-1][0] != side:
                        moves.append(position + self._get_position_from_idx((col_idx - 1, row_idx)))
        elif side == 'r':
            if row_idx > 0:
                if self.board[row_idx-1][col_idx][0] != side:
                    moves.append(position + self._get_position_from_idx((col_idx, row_idx - 1)))
            if row_idx <= 4:
                if col_idx < 8:
                    if self.board[row_idx][col_idx+1][0] != side:
                        moves.append(position + self._get_position_from_idx((col_idx + 1, row_idx)))
                if col_idx > 0:
                    if self.board[row_idx][col_idx-1][0] != side:
                        moves.append(position + self._get_position_from_idx((col_idx - 1, row_idx)))
        return moves
    
    def _generate_horse_moves(self, position_idx, side):
        moves = []
        opp = 'r' if side == 'b' else 'b'
        col_idx, row_idx = position_idx
        position = self._get_position_from_idx(position_idx)
        for action in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            new_row_idx = row_idx + action[1]
            new_col_idx = col_idx + action[0]
            if self._check_out_of_board(new_col_idx, new_row_idx):
                continue
            if self._hobbling_horse_leg(horse_pos_idx=position_idx, final_pos_idx=(new_col_idx, new_row_idx)):
                continue
            new_pos = self.board[new_row_idx][new_col_idx]

            if new_pos == '.' or new_pos[0] == opp:
                move = position + self._get_position_from_idx((new_col_idx, new_row_idx))
                moves.append(move)
        
        return moves
