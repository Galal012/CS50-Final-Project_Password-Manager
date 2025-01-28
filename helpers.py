from flask import render_template, flash


def apology(s):
    flash("ERROR OCCURED!")
    return render_template("apology.html", message = s)