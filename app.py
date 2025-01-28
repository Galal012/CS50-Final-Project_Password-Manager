from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///manager.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("Missing username!")
        
        row = db.execute("SELECT * FROM users WHERE username = ?;", username)
        if len(row) != 0:
            return apology("Username already exists!")
        
        password = request.form.get("password")
        confirmation = request.form.get("confirm-password")
        if not password or not confirmation:
            return apology("Missing password!")
        
        if password != confirmation:
            return apology("Passwords does not match!")
        
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", username, generate_password_hash(password))

        return redirect("/login")

    return render_template("register.html")