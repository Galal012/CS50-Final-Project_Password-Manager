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
        name = request.form.get("name")
        if not name:
            return apology("Missing name!")
        
        phone = request.form.get("phone")
        if not phone:
            return apology("Missing phone number!")

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
        
        gender = request.form.get("gender")
        if not gender:
            return apology("Missing gender!")
        gender = str(gender)
        
        db.execute(
            "INSERT INTO users (username, hash, name, phone, gender) VALUES (?, ?, ?, ?, ?);",
            username,
            generate_password_hash(password),
            name,
            phone,
            gender
        )

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
            "INSERT INTO accounts (user_id, company, username, password) VALUES (?, ?, ?, ?);",
            session["user_id"],
            company,
            username,
            password
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
        password = request.form.get("password")
        if not password:
            return redirect("/")
        return redirect("/myAccounts")

    companies = db.execute("SELECT company FROM accounts WHERE user_id = ?;", session["user_id"])
    return render_template("delete.html", companies=companies)


@app.route("/myAccounts", methods=["GET", "POST"])
@login_required
def myAccounts():
    if request.method == "POST":
        company = request.form.get("company")
        username = request.form.get("username")
        password = request.form.get("password")

        if not company and not username and not password:
            accounts = db.execute(
                "SELECT * FROM accounts WHERE user_id = ?;",
                session["user_id"]
            )
        
        elif not company and not username and password:
            accounts = db.execute(
                "SELECT * FROM accounts WHERE user_id = ? AND password = ?;", 
                session["user_id"], 
                password
            )

        elif not company and username and not password:
            accounts = db.execute(
                "SELECT * FROM accounts WHERE user_id = ? AND username = ?;", 
                session["user_id"], 
                username
            )

        elif not company and username and password:
            accounts = db.execute(
                "SELECT * FROM accounts WHERE user_id = ? AND username = ? AND password = ?;", 
                session["user_id"], 
                username,
                password
            )

        elif company and not username and not password:
            accounts = db.execute(
                "SELECT * FROM accounts WHERE user_id = ? AND company = ?;", 
                session["user_id"], 
                str(company)
            )

        elif company and not username and password:
            accounts = db.execute(
                "SELECT * FROM accounts WHERE user_id = ? AND company = ? AND password = ?;", 
                session["user_id"], 
                str(company),
                password
            )
        
        elif company and username and not password:
            accounts = db.execute(
                "SELECT * FROM accounts WHERE user_id = ? AND company = ? AND username = ?;", 
                session["user_id"], 
                str(company),
                username
            )

        else:
            accounts = db.execute(
                "SELECT * FROM accounts WHERE user_id = ? AND company = ? AND username = ? AND password = ?;", 
                session["user_id"], 
                str(company),
                username,
                password
            )

        if len(accounts) == 0:
            return apology("No matched accounts!")

        companies = db.execute("SELECT DISTINCT(company) FROM accounts WHERE user_id = ?;", session["user_id"])
        return render_template("myAccounts.html", accounts=accounts, companies=companies, type="POST")

    accounts = db.execute("SELECT * FROM accounts WHERE user_id = ?;", session["user_id"])
    companies = db.execute("SELECT DISTINCT(company) FROM accounts WHERE user_id = ?;", session["user_id"])
    return render_template("myAccounts.html", accounts=accounts, companies=companies, type="GET", size=len(accounts))


@app.route("/edit", methods=["POST"])
@login_required
def edit():
    account = db.execute("SELECT * FROM accounts WHERE id = ?;", request.form.get("account_id"))
    return render_template("edit.html", account=account)


@app.route("/edited", methods=["POST"])
@login_required
def edited():
    company = request.form.get("company").upper()
    if not company:
        return apology("Missing company!")
    
    username = request.form.get("username")
    if not username:
        return apology("Missing username!")
    
    password = request.form.get("password")
    if not password:
        return apology("Missing password!")
    
    account_id = request.form.get("account_id")
    account = db.execute("SELECT * FROM accounts WHERE id = ?", account_id)
    row = db.execute("SELECT * FROM accounts WHERE user_id = ? AND company = ? AND username = ?;", session["user_id"], company, username)
    if (len(row) != 0 and row != account) or (row == account and password == account[0]["password"]):
        return apology("Account already exists!")
    
    db.execute (
        "UPDATE accounts SET company = ?, username = ?, password = ? WHERE id = ?;",
        company,
        username,
        password,
        account_id
    )

    flash("Account editted successfully!")
    return redirect("/myAccounts")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            return apology("Missing name!")
        
        phone = request.form.get("phone")
        if not phone:
            return apology("Missing phone number!")

        username = request.form.get("username")
        if not username:
            return apology("Missing username!")
        
        account = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])[0]
        row = db.execute("SELECT * FROM users WHERE username = ?;", username)
        if len(row) == 1 and username != account["username"]:
            return apology("Username already exists!")
        
        gender = request.form.get("gender")
        if not gender:
            return apology("Missing gender!")
        gender = str(gender)

        if account["name"] == name and account["phone"] == phone and account["username"] == username and account["gender"] == gender:
            return apology("No changes occured!")
        
        db.execute(
            "UPDATE users SET name = ?, phone = ?, username = ?, gender = ? WHERE id = ?;",
            name,
            phone,
            username,
            gender,
            session["user_id"]
        )

        flash("Changes saved successfully!")
        return redirect("/")

    details = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
    return render_template("settings.html", info=details[0])


@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    if request.method == "POST":
        oldpass = request.form.get("old-password")
        newpass = request.form.get("new-password")
        confirmpass = request.form.get("confirm-new-password")

        if not oldpass or not newpass or not confirmpass:
            return apology("Missing password!")
        
        row = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
        if not check_password_hash(row[0]["hash"], oldpass):
            return apology("Incorrect old password!")
        
        if newpass != confirmpass:
            return apology("New passwords does not match!")
        
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?;",
            generate_password_hash(newpass),
            session["user_id"]
        )

        flash("Password changed successfully!")
        return redirect("/")

    return render_template("changePassword.html")