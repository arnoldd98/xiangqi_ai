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
'''
ROW_LENGTH = 10
COL_LENGTH = 9
COL = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
COL_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
ROW = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
START_FEN = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'

'''
    Helper class for board, which contains the current state of the Xiangqi board and possible moves it can take
'''
class Board:
    def __init__(self, possible_moves, fen=None):
        self.board = self.fen_to_board(fen) if fen else self.fen_to_board(START_FEN)
        self.moves = possible_moves
        print(fen)
        print(self.moves)
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

        # modify current board
        self.prev_board = copy.deepcopy(self.board)
        piece = self.get_piece(initial)
        self.board[initial_row_idx][initial_col_idx] = '.'
        self.board[final_row_idx][final_col_idx] = piece

        # check for available moves

    def undo(self):
        self.board = copy.deepcopy(self.prev_board)

    def get_piece(self, position):
        row_idx, col_idx = self._get_idx_from_position(position)
        return self.board[row_idx][col_idx]

    def generate_moves(self):
        legal_moves = {side: [] for side in ['r', 'b']}
        for row_idx, row in enumerate(self.board):
            for col_idx, piece in enumerate(row):
                assert piece[0] in ['r', 'b']
                side = piece[0]
                position_idx = (row_idx, col_idx)
                if piece[1] == 'K':
                    legal_moves[piece[0]].extend(self._generate_king_moves(position_idx, side))
                elif piece[1] == 'A':
                    legal_moves[piece[0]].extend(self._generate_advisor_moves(position_idx, side))
                elif piece[1] == 'R':
                    legal_moves[piece[0]].extend(self._generate_rook_moves(position_idx, side))
                elif piece[1] == 'C':
                    legal_moves[piece[0]].extend(self._generate_cannon_moves(position_idx, side))
                elif piece[1] == 'B':
                    legal_moves[piece[0]].extend(self._generate_elephant_moves(position_idx, side))
                elif piece[1] == 'P':
                    legal_moves[piece[0]].extend(self._generate_pawn_moves(position_idx, side))
                elif piece[1] == 'N':
                    legal_moves[piece[0]].extend(self._generate_horse_moves(position_idx, side))

    def _get_idx_from_position(self, position):
        row_idx = int(position[1])
        col_idx = COL.get(position[0])
        return row_idx, col_idx
    
    def _get_position_from_idx(self, position_idx):
        row_idx, col_idx = position_idx
        return COL_LETTERS[col_idx] + ROW[row_idx]

    def _fen_to_piece(self, fen_piece):
        if fen_piece.islower(): 
            return 'b' + fen_piece.upper()
        else:
            return 'r' + fen_piece.upper()

    def _generate_king_moves(self, position_idx, side):
        moves = []
        opp = 'r' if side == 'b' else 'b'
        if side == 'r':
            legal_positions = ['d2', 'e2', 'f2', 'd1', 'e1', 'f1', 'd0', 'e0', 'f0']
        elif side == 'b':
            legal_positions = ['d7', 'e7', 'f7', 'd8', 'e8', 'f8', 'd9', 'e9', 'f9']
        row_idx, col_idx = position_idx
        for action in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row_idx = row_idx + action[0]
            new_col_idx = col_idx + action[1]
            if new_row_idx > 8 or new_row_idx < 0 or new_col_idx > 9 or new_col_idx < 0:
                continue
            new_pos = self.board[new_row_idx][new_col_idx]
            if new_pos == '.' or new_pos[0] == opp:
                if new_pos in legal_positions:
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
        row_idx, col_idx = position_idx
        for action in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            new_row_idx = row_idx + action[0]
            new_col_idx = col_idx + action[1]
            if new_row_idx > 8 or new_row_idx < 0 or new_col_idx > 9 or new_col_idx < 0:
                continue
            new_pos = self.board[new_row_idx][new_col_idx]
            if new_pos == '.' or new_pos[0] == opp:
                if new_pos in legal_positions:
                    move = self._get_position_from_idx(position_idx) + new_pos
                    moves.append(move)
        return moves
    
    def _generate_rook_moves(self, position_idx, side):
        moves = []
        position = self._get_position_from_idx(position_idx)
        row_idx, col_idx = position_idx
        opp = 'r' if side == 'b' else 'b'
        
        # check for horizontal moves
        for direction in [-1, 1]:
            limit_x = col_idx
            while limit_x > 0 and limit_x < 9:
                new_pos = self.board[row_idx][limit_x]
                limit_x += direction
                if new_pos == '.':
                    moves.append(position + self._get_position_from_idx((row_idx, limit_x)))
                elif new_pos[0] == opp:
                    moves.append(position + self._get_position_from_idx((row_idx, limit_x)))
                elif new_pos[0] == side:
                    break

        # check for vertical moves
        for direction in[-1, 1]:
            limit_y = row_idx
            while limit_y > 0 and limit_y < 10:
                new_pos = self.board[limit_y][col_idx]
                limit_y += direction
                if new_pos == '.':
                    moves.append(position + self._get_position_from_idx((limit_y, col_idx)))
                elif new_pos[0] == opp:
                    moves.append(position + self._get_position_from_idx((limit_y, col_idx)))
                elif new_pos[0] == side:
                    break

    def _generate_cannon_moves(self, position_idx, side):
        moves = []
        position = self._get_position_from_idx(position_idx)
        row_idx, col_idx = position_idx
        opp = 'r' if side == 'b' else 'b'

        # check for horizontal moves
        skipped = False
        for direction in [-1, 1]:
            limit_x = col_idx
            while limit_x > 0 and limit_x < 9:
                new_pos = self.board[row_idx][limit_x]
                if new_pos == '.':
                    moves.append(position + self._get_position_from_idx((row_idx, limit_x)))
                    limit_x += direction
                elif new_pos != '.' and not skipped:
                    skipped = True
                    limit_x += direction
                elif new_pos == opp and skipped:
                    moves.append(position + self._get_position_from_idx((row_idx, limit_x)))
                    break
                elif new_pos == side and skipped:
                    break
        
        # check for vertical moves
        skipped = False
        for direction in [-1, 1]:
            limit_y = row_idx
            while limit_y > 0 or limit_y < 10:
                new_pos = self.board[limit_y][col_idx]
                if new_pos == '.':
                    moves.append(position + self._get_position_from_idx((limit_y, col_idx)))
                    limit_y += direction
                elif new_pos != '.' and not skipped:
                    skipped = True
                    limit_y += direction
                elif new_pos == opp and skipped:
                    moves.append(position + self._get_position_from_idx((limit_y, col_idx)))
                    break
                elif new_pos == side and skipped:
                    break
        return moves
    
    def _generate_elephant_moves(self, position_idx, side):
        moves = []
        opp = 'r' if side == 'b' else 'b'
        if side == 'r':
            legal_positions = ['c0', 'g0', 'a2', 'e2', 'i2', 'c4', 'g4']
        elif side == 'b':
            legal_positions = ['c9', 'g9', 'a7', 'e7', 'i7', 'c5', 'g5']
        row_idx, col_idx = position_idx
        for action in [(2, 2), (2, -2), (-2, 2), (-2, -2)]:
            new_row_idx = row_idx + action[0]
            new_col_idx = col_idx + action[1]
            if new_row_idx > 8 or new_row_idx < 0 or new_col_idx > 9 or new_col_idx < 0:
                continue
            new_pos = self.board[new_row_idx][new_col_idx]
            if new_pos == '.' or new_pos[0] == opp:
                if new_pos in legal_positions:
                    move = self._get_position_from_idx(position_idx) + new_pos
                    moves.append(move)
        return moves
    
    def _generate_pawn_moves(self, position_idx, side):
        moves = []
        opp = 'r' if side == 'b' else 'b'
        row_idx, col_idx = position_idx
        position = self._get_position_from_idx(position_idx)

        if side == 'r':
            if row_idx < 9:
                moves.append(position + self._get_position_from_idx((row_idx + 1, col_idx)))
            if row_idx >= 5:
                if col_idx < 8:
                    moves.append(position + self._get_position_from_idx((row_idx, col_idx + 1)))
                if col_idx > 0:
                    moves.append(position + self._get_position_from_idx((row_idx, col_idx - 1)))
        elif side == 'b':
            if row_idx > 0:
                moves.append(position + self._get_position_from_idx((row_idx - 1, col_idx)))
            if row_idx <= 4:
                if col_idx < 8:
                    moves.append(position + self._get_position_from_idx((row_idx, col_idx + 1)))
                if col_idx > 0:
                    moves.append(position + self._get_position_from_idx((row_idx, col_idx - 1)))
        return moves
    
    def _generate_horse_moves(self, position_idx, side):
        moves = []
        opp = 'r' if side == 'b' else 'b'
        row_idx, col_idx = position_idx
        position = self._get_position_from_idx(position_idx)
        for action in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            new_row_idx = row_idx + action[0]
            new_col_idx = col_idx + action[1]
            if new_row_idx > 8 or new_row_idx < 0 or new_col_idx > 9 or new_col_idx < 0:
                continue
            new_pos = self.board[new_row_idx][new_col_idx]

            if action == (1, 2) or action == (-1, 2):
                blocker_idx = (new_row_idx, new_col_idx + 1)
            elif action == (1, -2) or action == (-1, -2):
                blocker_idx = (new_row_idx, new_col_idx - 1)
            elif action == (2, 1) or action == (2, -1):
                blocker_idx = (new_row_idx + 1, new_col_idx)
            elif action == (-2, 1) or action == (-2, -1):
                blocker_idx = (new_row_idx - 1, new_col_idx)
            if self.board[blocker_idx[0]][blocker_idx[1]] != '.':
                continue

            if new_pos == '.' or new_pos[0] == opp:
                move = position + self._get_position_from_idx((new_row_idx, new_col_idx))
                moves.append(move)
        return moves

        




        

