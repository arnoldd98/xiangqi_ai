from flask import Flask, render_template, request, redirect, url_for, jsonify
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/ai/move', methods=['POST'])
def ai_move():
    fen, moves = request.form['fen'], request.form.getlist('possible_moves[]')
    if len(moves) == 0:
        return jsonify({'move': None})
    rand_idx = random.randrange(0, len(moves))
    results = {'move': moves[rand_idx]}
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)