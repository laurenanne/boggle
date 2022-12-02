from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


boggle_game = Boggle()
board_game = 'board'


@app.route('/')
def index():
    """Return Homepage with start button that creates board"""
    return render_template("start.html")


@app.route('/boggle')
def play_game():
    """set up board game with form to enter a word"""
    board = boggle_game.make_board()
    session[board_game] = board
    return render_template("index.html", board=board)


@app.route('/check')
def check_word():
    "check validity of word"
    board = session[board_game]
    word = request.args['word']

    answer = boggle_game.check_valid_word(board, word)
    return jsonify({'answer': answer})


count = 0
scores = []


@app.route('/post-score', methods=["POST"])
def post_word():
    currentScore = request.json["total"]
    scores.append(currentScore)
    highscore = max(scores)
    session['highscore'] = highscore

    global count
    count = count+1

    return jsonify({"highscore": highscore, 'count': count})
