from board import Board
from prettyprinter import pprint
from collections import Counter

''' 
    Test the board class
'''
BASE_FEN = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'

def base_tests():
    base_board = Board(fen=BASE_FEN)
    moves = base_board.generate_moves('b')
    # pprint(base_board.board)
    # print('All possible base moves: ', moves)

    test_rook_moves(board=base_board, moves=moves)
    test_horse_moves(board=base_board, moves=moves)
    test_elephant_moves(board=base_board, moves=moves)
    test_advisor_moves(board=base_board, moves=moves)
    test_general_moves(board=base_board, moves=moves)
    test_cannon_moves(board=base_board, moves=moves)
    test_pawn_moves(board=base_board, moves=moves)

    print('All base cases passed!')

def custom_tests():
    test_advisor_moves()
    print('All custom cases passed!')

def test_rook_moves(board=None, moves=None):
    if moves != None:   # base case
        rook = 'bR'
        positions = board.get_position(rook)
        assert set(positions) == set(['a9', 'i9'])

        rook_pos = 'a9'
        rook_moves = []
        for move in moves:
            if move[0:2] == rook_pos:
                rook_moves.append(move)
        assert set(rook_moves) == set(['a9a8', 'a9a7'])

def test_horse_moves(board=None, moves=None):
    if moves != None:   # base case
        horse = 'bN'
        positions = board.get_position(horse)
        assert set(positions) == set(['b9', 'h9'])
        
        horse_pos = 'b9'
        horse_moves = []
        for move in moves:
            if move[0:2] == horse_pos:
                horse_moves.append(move)
        assert set(horse_moves) == set(['b9a7', 'b9c7'])

def test_elephant_moves(board=None, moves=None):
    if moves != None:   # base case
        elephant = 'bB'
        positions = board.get_position(elephant)
        assert set(positions) == set(['c9', 'g9'])

        elephant_pos = 'c9'
        elephant_moves = []
        for move in moves:
            if move[0:2] == elephant_pos:
                elephant_moves.append(move)
        assert set(elephant_moves) == set(['c9a7', 'c9e7'])

def test_advisor_moves(board=None, moves=None):
    if moves != None:   # base case
        advisor = 'bA'
        positions = board.get_position(advisor)
        assert set(positions) == set(['d9', 'f9'])

        advisor_pos = 'd9'
        advisor_moves = []
        for move in moves:
            if move[0:2] == advisor_pos:
                advisor_moves.append(move)
        assert set(advisor_moves) == set(['d9e8'])
    else: 
        board = Board(fen='rnbakabnr/9/4c2c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/4K4/RNBA1ABNR',
                     current_side='r')
        moves = board.generate_moves('r')
        advisor = 'rA'
        positions = board.get_position(advisor)
        assert set(positions) == set(['d0', 'f0'])

        advisor_pos = 'f0'
        advisor_moves = []
        for move in moves:
            if move[0:2] == advisor_pos:
                advisor_moves.append(move)
        assert len(advisor_moves) == 0


def test_general_moves(board=None, moves=None):
    if moves != None:   # base case
        general = 'bK'
        positions = board.get_position(general)
        assert set(positions) == set(['e9'])

        general_pos = 'e9'
        general_moves = []
        for move in moves:
            if move[0:2] == general_pos:
                general_moves.append(move)
        assert set(general_moves) == set(['e9e8'])

def test_cannon_moves(board=None, moves=None):
    if moves != None:   # base case
        cannon = 'bC'
        positions = board.get_position(cannon)
        assert set(positions) == set(['b7', 'h7'])

        cannon_pos = 'b7'
        cannon_moves = []
        for move in moves:
            if move[0:2] == cannon_pos:
                cannon_moves.append(move)
        assert set(cannon_moves) == set(['b7a7', 'b7c7', 'b7d7', 'b7e7', 'b7f7', 'b7g7',
                                         'b7b8', 'b7b6', 'b7b5', 'b7b4', 'b7b3', 'b7b0'])
                            
def test_pawn_moves(board=None, moves=None):
    if moves != None:   # base case
        pawn = 'bP' 
        positions = board.get_position(pawn)
        assert set(positions) == set(['a6', 'c6', 'e6', 'g6', 'i6'])

        pawn_pos = 'a6'
        pawn_moves = []
        for move in moves:
            if move[0:2] == pawn_pos:
                pawn_moves.append(move)
        assert set(pawn_moves) == set(['a6a5'])
    
def test_checkmate():
    fen = 'rnbakabnr/9/1c5c1/p1p1C1p1p/9/4C4/P1P1P1P1P/9/9/RNBAKABNR'   # double cannon checkmate
    board = Board(fen=fen)
    assert board.is_checkmate()

    print('Checkmate test passed!')

def test_check():
    fen_1 = 'rnbakabnr/9/1c6c/p1p1p1p1p/9/4C4/P1P1P1P1P/1C7/9/RNBAKABNR'
    board1 = Board(fen=fen_1)
    assert board1.is_check(board1.side)


    fen_2 = 'rn1akabnr/9/1c2b3c/p1p1p1p1p/9/4C4/P1P1P1P1P/1C7/9/RNBAKABNR'
    board2 = Board(fen=fen_2)
    assert not board2.is_check(board2.side)

    fen_3 = '3a1a3/3k4r/n3b1ccb/2p3p1p/C8/9/P1P1P1P1P/4r4/R8/2BAKABNR'
    board3 = Board(fen=fen_3)
    assert board3.is_check('r')

    fen_4 = '2ba1abnr/r2k5/n8/p1pC2p1p/9/4c1C2/PcP1P1P1P/6N2/9/RNBAKAB1R'
    board4 = Board(fen=fen_4)
    assert board4.is_check('r')
    print('Check test passed!')

if __name__ == "__main__":
    base_tests()
    custom_tests()
    test_checkmate()
    test_check()