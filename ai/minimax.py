from math import inf
import random
from ai.board import Board
from ai.evaluation import basic_evaluation, points_evaluation

'''
    Simple greedy approach that returns the move that produces the best basic evaluation result
'''
def greedy(board, maximizing_colour):
    moves = board.get_moves()
    best_move = None
    best_score = -inf
    for move in moves:
        board.make_move(move, change_side=False)
        score = basic_evaluation(board, maximizing_colour)
        board.undo(change_side=False)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

hashmap = dict()
hash_counts = 0
buffer = []
'''
    Transposition table to hold previously explored boards. Works similarly to a cache.
'''
def add_to_hashmap(hashkey, hashmap_size, val):
    global hash_counts, hashmap, buffer
    if hash_counts == hashmap_size:
        for key in buffer[:int(hashmap_size/10)]:
            hashmap.pop(key)
        buffer = buffer[int(hashmap/10):]
    else:
        hash_counts += 1 
        
    hashmap[hashkey] = val
    buffer.append(hashkey)

'''
    Minimax algorithm with alpha-beta pruning
'''
def minimax(board, depth, alpha, beta, maximizing_player, maximizing_colour, hashmap_size=10000):
    hashkey = board.side + ' ' + board.get_fen()
    if hashkey in hashmap:
        return hashmap[hashkey]
    
    # moves = board.get_moves()
    moves = board.get_ordered_moves(board.side)
    if depth == 0 or board.is_checkmate(): # if no possible moves, checkmate
        return None, points_evaluation(board, maximizing_colour)
    best_move = None
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
        add_to_hashmap(hashkey, hashmap_size, (best_move, max_eval))
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
        add_to_hashmap(hashkey, hashmap_size, (best_move, min_eval))
        return best_move, min_eval  

