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

