from math import inf
import random
from ai.board import Board
from ai.evaluation import basic_evaluation
# from evaluation import basic_evaluation

'''
    Minimax algorithm with alpha-beta pruning
'''
def minimax(board, depth, alpha, beta, maximizing_player, maximizing_colour):
    moves = board.get_moves()
    if depth == 0 or len(moves) == 0: # if no possible moves, checkmate
        return None, basic_evaluation(board, maximizing_colour)
    best_move = random.choice(moves)
    if maximizing_player:
        max_eval = -inf
        for move in moves:
            assert board.side == maximizing_colour
            board.make_move(move, change_side=True)
            current_eval = minimax(board, depth-1, alpha, beta, False, maximizing_colour)[1]
            board.undo(change_side=True)
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
        return best_move, max_eval
    
    else:
        min_eval = inf
        for move in moves:
            assert board.side == 'r'
            board.make_move(move, change_side=True)
            current_eval = minimax(board, depth-1, alpha, beta, True, maximizing_colour)[1]
            board.undo(change_side=True)
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        
        return best_move, min_eval  