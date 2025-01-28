from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

import secrets
import string

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
@login_required
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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.clear()

        username = request.form.get("username")
        if not username:
            return apology("Missing username!")
        
        password = request.form.get("password")
        if not password:
            return apology("Missing password!")
        
        row = db.execute("SELECT * FROM users WHERE username = ?;", username)
        if len(row) != 1 or not check_password_hash(row[0]["hash"], password):
            return apology("invalid username and/or password")
        
        session["user_id"] = row[0]["id"]
        return redirect("/")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        company = request.form.get("company").upper()
        if not company:
            return apology("Missing company!")
        
        username = request.form.get("username")
        if not username:
            return apology("Missing username!")
        
        password = request.form.get("password")
        if not password:
            return apology("Missing password!")
        
        row = db.execute("SELECT * FROM accounts WHERE user_id = ? AND company = ? AND username = ?;", session["user_id"], company, username)
        if len(row) != 0:
            return apology("Account already exists!")
        
        db.execute(
            "INSERT INTO accounts (user_id, company, username, hash) VALUES (?, ?, ?, ?);",
            session["user_id"],
            company,
            username,
            generate_password_hash(password)
        )

        flash("Account added successfully!")
        return redirect("/")

    return render_template("add.html")


@app.route('/generate_password')
def generate_password():
    length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    return jsonify(password=password)


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        company = request.form.get("company")
        if not company:
            return apology("Missing company!")
        company = str(company)
        
        username = request.form.get("username")
        if not username:
            return apology("Missing username!")
        
        row = db.execute("SELECT * FROM accounts WHERE user_id = ? AND company = ? AND username = ?;", session["user_id"], company, username)
        if len(row) == 0:
            return apology("Account does not exist!")
        
        db.execute("DELETE FROM accounts WHERE user_id = ? AND company = ? AND username = ?;", session["user_id"], company, username)

        flash("Account deleted successfully!")
        return redirect("/")

    companies = db.execute("SELECT company FROM accounts WHERE user_id = ?;", session["user_id"])
    return render_template("delete.html", companies=companies)