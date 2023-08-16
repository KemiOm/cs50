# Kemi: buy, index, function, index.html, quote/quoted.html, buy.html
# both did register
# Bayan: sell, history, function, history.html, register.html

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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

    # get all personal info
    info = db.execute("SELECT symbol, SUM(shares) AS shares2, price FROM data WHERE id = ? GROUP BY symbol HAVING shares2 > 0", session["user_id"])

    # grab cash
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = cash[0]["cash"]
    if not cash:
        return apology("ohh so try again", 403)
    # total = shares of each stock (from table ) x the current price (dictionary use lookup)
    total = cash
    for item in info:
        # name of our dictionary
        ourdict = lookup(item["symbol"])
        item["price"] = ourdict["price"]
        item["name"] = ourdict["name"]
        total += item["price"] * item["shares2"]
    return render_template("index.html", info=info, total=usd(total), cash=usd(cash))

    # Display HTML table with all stocks owned (string), # of shares in each stock (int), current price of stock


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        stock = lookup(request.form.get("symbol"))
        shares = int(request.form.get("shares"))
        # check if its they submitted the right thing, question do I need to call quote where symbol is established?
        if not stock:return apology("invalid stock symbol", 403)
        if shares < 0:
            return apology("invalid amount", 403)
        # ensure user has enough cash to afford stock
        # local variable
        cash = (db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"]) [0]["cash"])
        price = stock["price"]
        symbol = stock["symbol"]
        # math
        total = (shares * price)
        if total < 0:
            #if user cant afford then retuen apology to let them know
            return apology("you're broke", 403)
        #add new stock purchasae to user's portfolio
        else:
            db.execute("INSERT INTO data (id, symbol, shares, price) VALUES (?,?,?,?)", session["user_id"], symbol, shares, price)
            #when user has enough cash for purchase --> run SQL ststament you need on database to purchase stock
            #update user's cash to reflect purchase
            cash =  cash - total
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
            return redirect("/")


@app.route("/history")
@login_required
def history():
    portfolio = db.execute("SELECT symbol, shares, price, transactions FROM data WHERE id = ?", session["user_id"])
    return render_template("history.html", portfolio = portfolio)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        # checks against string for hash password that already in your database
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    # get to quote page
    if request.method == "GET":
        return render_template("quote.html")

    # look up function walkthrough/ now POST
    else:
        dictionary = lookup(request.form.get("symbol"))
        #check it exists not is a null check
        if dictionary == None:
            return apology("invalid stock", 403)

        # create variables
        name = dictionary["name"]
        price = dictionary["price"]
        symbol = dictionary["symbol"]

        return render_template("quoted.html", name = name, price = usd(price), symbol = symbol)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # looks like login

    # make sure there no repeat
    if request.method == "POST":

        # make sure username is inputted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # make sure password is inputted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        count = 0
        for x in request.form.get("password"):
            if x.isdigit():
                count+=1
        if count == 0:
            return apology("You need a number",403)
        if request.form.get("password").isdigit():
            return apology("You also need letters", 403)

        #check
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password must match", 403)

        # save login info
        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))

        #go through database check to make sure username are unique
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # check username
        if len(rows) > 0:
            return apology("invalid username and/or password", 403)

        # insert username and password
        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, hash)

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    #display form --> get stock to sell
    # get all personal info
    info =  db.execute("SELECT symbol, SUM(shares) AS shares, price FROM data WHERE id = ? GROUP BY symbol" , session["user_id"])
    # grab caash
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = cash[0]["cash"]
    # start actually selling
    if request.method == "GET":
        return render_template("sell.html")
    else:
        # for the information from the text boxes
        stock = lookup(request.form.get("symbol"))
        shares = int(request.form.get("shares"))
        if not stock:
            return apology("You did it wrong", 403)
        if shares < 1:
            return apology("invalid amount", 403)
        symbol = stock["symbol"]
        usershares = db.execute("SELECT SUM(shares) AS sumshares FROM data WHERE id = ? AND symbol = ?", session["user_id"], symbol)[0]["sumshares"]
        print(usershares)
        if usershares < shares:
            return apology("You don't have enough", 403)
        else:
            price = stock["price"]
            total =  (shares * price)
            shares = -(shares)
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]


        # math

        db.execute("INSERT INTO data (id, symbol, shares, price) VALUES (?,?,?,?)", session["user_id"], symbol, shares, price)
                #when user has enough cash for purchase --> run SQL ststament you need on database to purchase stock
                #update user's cash to reflect purchase
        cash =  total + cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
        return redirect("/")

