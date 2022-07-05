from boggle import Boggle
from flask import Flask, jsonify, render_template_string,request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = "chickenzarecool21837"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


boggle_game = Boggle()

@app.route("/")
def start_page():
    """Clear the session of responses."""

    session["board"]

    return redirect("/start")

@app.route("/start")
def show_page():
    board = boggle_game.make_board()

    session["board"] = board
    # responses.append(board)
    return render_template('start.html',  responses=session["board"])

@app.route("/check-word")
def check_word():
    the_word = request.args.get("word")
    responses = session["board"]
    resp = boggle_game.check_valid_word(the_word,responses)
    

    return jsonify({"result": resp})


