import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from newsapi import NewsApiClient

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__, static_url_path='/static')
# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# Make sure API key is set



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

@app.route("/know")
def know():
    return render_template("know.html")

@app.route("/news")
def news():
    newsapi = NewsApiClient(api_key="a8013cb218384c2e991b9f081b9e7ba6")
    print(newsapi)
    topheadlines = newsapi.get_top_headlines(language="en", sources="the-wall-street-journal")

    articles = topheadlines['articles']
    mylist = []

    for i in range(len(articles)):
        myarticles = articles[i]
        newszip = {}
        newszip["title"]= myarticles["title"]
        newszip["desc"]= myarticles["description"]
        newszip["author"]=myarticles["author"]
        mylist.append(newszip)

    return render_template('news.html', context = mylist)

if __name__== "__main__":
    app.run(debug=True)


@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM register WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        # checks against string for hash password that already in your database
        if len(rows) != 1 or not (rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return render_template("comp.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # looks like login
    # make sure there no repeat
    if request.method == "POST":

        # make sure username is inputted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("email"):
            return apology("must provide email", 400)
        # make sure password is inputted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("phone"):
            return apology("must provide phone", 400)


        #check
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password must match", 400)

        # save login info
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")

        #go through database check to make sure username are unique
        rows = db.execute("SELECT * FROM register WHERE username = ?", request.form.get("username"))
        # check username
        if len(rows) > 0:
            return apology("invalid username and/or password", 400)

        # insert username and password
        db.execute("INSERT INTO register (username, email, password, phone) VALUES(?,?,?,?)", username, email, password, phone)

        return render_template("comp.html")
    else:
        return render_template("register.html")
