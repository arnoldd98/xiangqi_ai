from cgitb import reset
from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import sys, os
from ai.minimax import minimax, greedy
from ai.board import Board
import time

times_called = 0
total_time = 0

EASY_CONFIG = {'algo': 'greedy'}
MEDIUM_CONFIG = {'algo': 'minimax', 'depth': 1}
HARD_CONFIG = {'algo': 'minimax', 'depth': 3}
config = HARD_CONFIG

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/ai/move', methods=['POST'])
def ai_move():
    global times_called, total_time

    times_called += 1
    fen, moves = request.form['fen'], request.form.getlist('possible_moves[]')
    if len(moves) == 0:
        return jsonify({'move': None})
    inf = float('inf')
    
    start = time.time() # measure time of execution for algorithm
    board = Board(fen)
    
    if config['algo'] == 'greedy':
        best_move = greedy(board, board.side)
        print(best_move)
    elif config['algo'] == 'minimax':
        best_move = minimax(board, config['depth'], -inf, inf, True, board.side)[0]

    end = time.time()
    time_taken = end - start
    print('Time taken to run minimax: ', time_taken)
    total_time += time_taken
    print('Average times so far: ', total_time / times_called)
    
    results = {'move': best_move}
    return jsonify(results)

@app.route('/ai/set_difficulty', methods=['POST'])
def set_difficulty():
    global config
    difficulty = request.form['difficulty']
    print('Set game mode: ', difficulty)
    if difficulty == 'Beginner':
        config = EASY_CONFIG
    elif difficulty == 'Intermediate':
        config = MEDIUM_CONFIG
    elif difficulty == 'Advanced':
        config = HARD_CONFIG

    return jsonify({'success': True})

if __name__ == "__main__":
    app.run(debug=True)