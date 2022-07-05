from crypt import methods
from boggle import Boggle
from flask import Flask, jsonify, render_template_string,request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = "chickenzarecool21837"

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)


boggle_game = Boggle()

# @app.route("/")
# def start_page():
#     """Clear the session of responses."""

#     session["board"]

#     return redirect("/start")

@app.route("/")
def show_page():
    """show the board"""

    board = boggle_game.make_board()

    highscore = session.get("highscore",0)
    num_play = session.get("num_play",0)

    session["board"] = board
    # responses.append(board)
    return render_template('start.html',  board=board, highscore=highscore,num_play=num_play)

@app.route("/check-word")
def check_word():
    """check if the word is valid"""
    the_word = request.args.get("word")
    board = session["board"]
    resp = boggle_game.check_valid_word(board,the_word)
    

    return jsonify({"result": resp})

@app.route("/show-score", methods=["POST"])
def show_score():
    score= request.json["score"]
    breakpoint()
    # import pdb; pdb.set_trace()
    highscore = session.get("highscore",0)
    num_play = session.get("num_play",0)

    session["highscore"]= max(score, highscore)
    session["num_play"]= num_play + 1
    return jsonify(newRecored=score)

