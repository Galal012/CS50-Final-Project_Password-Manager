from flask import render_template, flash, session, redirect
from functools import wraps


def apology(s):
    flash("ERROR OCCURED!")
    return render_template("apology.html", message = s)


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorator