files: [app.py]
url: https://github.com/code50/69874313/blob/main/Project/README.md#L2
window: [terminal]


# Project
Money over Matter a website dedicated to teaching people about personal finance. This was inspired by our club called Smart Women Securities.
# How To
To run the website make sure to access the folder itself called Project. Use the command cd Project in the terminal. Once, you've succesfully accessed the folder use the command flask run this will provide a link to the website and cmd + link to access this in a seperate tab.
# Background and More How To:
Most people are unfamiliar with using API, API's are most for connectivity the goal of an API is too also for a developer to use other products and services without necessarily knowing how these services are implemented. For this website a news API is used from the Wall Street Journal.
To use an API a user needs to run these to commands in there terminal.
`pip install flask`
`pip install newsapi-python`
Once installed in the app.py file users need to import into the app.py.
`from newsapi import NewsApiClient`
this grants access to your codespace attaches it to the project it's needed
You must also establish the newsapi as a variable in python under the html template you want it to appear on.
For the project this was news.HTML
# Folders
Before starting and downloading the zip file make sure to include the static folder and inside needs to be the style.css file and all the images these files don't change regardless and will be group seperate away from the other files. The images also need to be downloaded and stored under img or else the links throughout the website will not work. All of the image are simply named. The other subfolder necessary is template this contains all of the templates/ HTML files sued throughout the project they are all completed.
# Layout.HTML
This is the standard format for all the pages.
Using jinga code a user can not have to repeat code already established on all the other pages.
Things that we want to appear on every website page is the link to the style sheet, the bootstrap links, the navigation bar, and google font links
 To link Jinga to other parts of the website we established a
`{% block main %}`

`{% endblock %}`
In between that statement is where the what's created on the other HTML templates will appear.
At the beginning of all the templates on the website aside from layout.html there will be a `{% extends "layout.html" %}`
this is to indicate that this is continuation of the next field
# Apology
Under `templates/`. In `login.html` is, essentially, just an HTML form, stylized with [Bootstrap](http://getbootstrap.com/). In `apology.html`, meanwhile, is a template for an apology. Recall that `apology` in `helpers.py` took two arguments: `message`, which was passed to `render_template` as the value of `bottom`, and, optionally, `code`, which was passed to `render_template` as the value of `top`.

# NavBar
The navbar contains links to all the templates on the page aside from apology.html and comp.html because these are responses to things done incorrectly. Apology will appear when a user makes a mistake registering or logining. Comp.html will appear when a user has successfully registered for the website along with a new message.
Money Over Matter is the link to the index page. Register, Login, Quiz, all correspond to their respective HTML pages and Basics corresponds to the know.html

# Index
Nav bar and basic design deatils are linked to the original layout.html
Homepage will greet users with the title of the website, the website name, and the main mission
Make sure to insert the photo called women.png and have it kept in a file called static and another one called img
From there users can navigate around the website to check other things.

# Register
The Register page includes the following boxes
1. Username
2. Password
3. Check Password
3. email
4. phone number
User needs to create an original username and password or else an error will appear on the screen. Passwords must match or else error will occur.
Email must inputted in email format, and a phone number needs to be added as well. Usernames that occur mutiple times will be blocked from creating a new account
Phone number needs to be added as well. Once registered you will be redirected to a new screen welcom ing you and from there you are free to explore the rest of the website. In the app.py a SQL database is created and already linked to the website. All of the information entered will be stored for when the user decides to sign in. All the info is inserted as well.

# Login
Login follows a simolier layout with a user being able to login themselves with the same username and password as before.
# Quiz
on financial basic literacy
The general information to pass the quiz is included on the basics page
Select buttons that correspond with the following questions
If the answer is wrong the buttton will turn red
If the answer is correct the button will turn green
At the end of the quiz users are prompted to look at the basic page and navigate to there
DONE BY KEMI

# Basics
Background image is stored in the img folder under static

# Financial News
latest news and websites for people to get additional information on how to save money
news API explained in the background

# APP.PY
Atop the file are a bunch of imports, among them CS50's SQL module and a few helper functions
for basics basics the render template is already done along with the get and post
For Login and Register the sequel table is already referred to and people who login and register will be given access to it

The News API layout is also done there



