from cgitb import reset
from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import sys, os
from ai.minimax import minimax
from ai.board import Board
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/ai/move', methods=['POST'])
def ai_move():
    fen, moves = request.form['fen'], request.form.getlist('possible_moves[]')
    if len(moves) == 0:
        return jsonify({'move': None})
    # rand_idx = random.randrange(0, len(moves))
    # results = {'move': moves[rand_idx]}
    inf = float('inf')
    
    start = time.time() # measure time of execution for algorithm

    best_move = minimax(Board(fen=fen), 3, -inf, inf, True, 'b')[0]

    end = time.time()
    print('Time taken to run minimax: ', end - start)
    results = {'move': best_move}
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)