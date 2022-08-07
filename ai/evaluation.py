'''
    Helper file which contains evaluation functions to score current board
'''

def basic_evaluation(board, side):
    '''
        Evaluate the current board using basic heuristic
        Return a score between -100 and 100
    '''
    assert side == 'r' or side == 'b'
    opp = 'r' if side == 'b' else 'b'
    score = 0 
    for row in board.board:
        for piece in row:
            if piece[0] == side:
                score += 1
            elif piece[0] == opp:
                score -= 1
    return score

# piece evaluation scores as referenced from: 
# 'Using AdaBoost to Implement Chinese Chess Evaluation Functions'
# https://docplayer.net/27544684-Using-adaboost-to-implement-chinese-chess-evaluation-functions.html
PIECE_SCORE = {'K': 30, 'P': 3, 'A': 6, 'B': 6, 'N': 12, 'C': 13.5, 'R': 27}
PIECE_POS_SCORE = {
    'P': [[0,  0,  0,  0,  0,  0,  0,  0,  0],
          [0,  0,  0,  0,  0,  0,  0,  0,  0],
          [0,  0,  0,  0,  0,  0,  0,  0,  0],
          [0,  0, -2,  0,  4,  0, -2,  0,  0],
          [2,  0,  8,  0,  8,  0,  8,  0,  2],
          [6,  12, 18, 18, 20, 18, 18, 12, 6],
          [10, 20, 30, 34, 40, 34, 30, 20, 10],
          [14, 26, 42, 60, 80, 60, 42, 26, 14],
          [18, 36, 56, 80, 120, 80, 56, 36, 18],
          [0,  3,  6,  9,  12,  9,  6,  3,  0]],
    'N': [[0, -4, 0, 0, 0, 0, 0, -4, 0],
          [0, 2, 4, 4, -2, 4, 4, 2, 0],
          [4, 2, 8, 8, 4, 8, 8, 2, 4],
          [2, 6, 8, 6, 10, 6, 8, 6, 2],
          [4, 12, 16, 14, 12, 14, 16, 12, 4],
          [6, 16, 14, 18, 16, 18, 14, 16, 6],
          [8, 24, 18, 24, 20, 24, 18, 24, 8],
          [12, 14, 16, 20, 18, 20, 16, 14, 12],
          [4, 10, 28, 16, 8, 16, 28, 10, 4],
          [4, 8, 16, 12, 4, 12, 16, 8, 4]],
    'R': [[-2, 10, 6, 14, 12, 14, 6, 10, -2],
          [8, 4, 8, 16, 8, 16, 8, 4, 8],
          [4, 8, 6, 14, 12, 14, 6, 8, 4],
          [6, 10, 8, 14, 14, 14, 8, 10, 6],
          [12, 16, 14, 20, 20, 20, 14, 16, 12],
          [12, 14, 12, 18, 18, 18, 12, 14, 12],
          [12, 18, 16, 22, 22, 22, 16, 18, 12],
          [12, 12, 12, 18, 18, 18, 12, 12, 12],
          [16, 20, 18, 24, 26, 24, 18, 20, 16],
          [14, 14, 12, 18, 16, 18, 12, 14, 14]],
    'C': [[0, 0, 2, 6, 6, 6, 2, 0, 0],
          [0, 2, 4, 6, 6, 6, 4, 2, 0],
          [4, 0, 8, 6, 10, 6, 8, 0, 4],
          [0, 0, 0, 2, 4, 2, 0, 0, 0],
          [-2, 0, 4, 2, 6, 2, 4, 0, -2],
          [0, 0, 0, 2, 8, 2, 0, 0, 0],
          [0, 0, -2, 4, 10, 4, -2, 0, 0],
          [2, 2, 0, -10, -8, -10, 0, 2, 2],
          [2, 2, 0, -4, -14, -4, 0, 2, 2],
          [6, 4, 0, -10, -12, -10, 0, 4, 6]]    }

def points_evaluation(board, side):
    '''
        Evaluate the current board using points heuristic. 
        Each type of piece has a set number of points 
        Return a score between -100 and 100
    '''


    assert side == 'r' or side == 'b'
    opp = 'r' if side == 'b' else 'b'
    score = 0 
    for row_idx, row in enumerate(board.board):
        for col_idx, piece in enumerate(row):
            if piece[0] == '.':
                continue
            piece_type = piece[1]

            if piece[0] == side:
                if side == 'r':  
                    side_row_idx = 10 - row_idx
                score += PIECE_SCORE[piece_type]
                if piece_type in PIECE_POS_SCORE.keys():
                    score += PIECE_POS_SCORE[piece_type][side_row_idx][col_idx]
            elif piece[0] == opp:
                if opp == 'r':
                    side_row_idx = 10 - row_idx
                score -= PIECE_SCORE[piece_type]
                if piece_type in PIECE_POS_SCORE.keys():
                    score -= PIECE_POS_SCORE[piece_type][side_row_idx][col_idx]


    if board.is_check(side):
        score -= 50
    return score

