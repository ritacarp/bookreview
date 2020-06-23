from flask import render_template, flash, redirect, request, url_for
from app import app, grBookList
from app.forms import LoginForm, RegisterForm
from app.helpers import grLookupByID
import psycopg2
import os
import random

@app.route('/')
@app.route('/index')

def index():

    # http://www.datasciencemadesimple.com/strip-lstriprstrip-strip-function-python/
    # To strip off leading zeros - I googled python strip leading zeros
    
    # To shuffle a list
    # https://note.nkmk.me/en/python-random-shuffle/
    
    randomList = grBookList.copy()
    random.shuffle(randomList)
    # print("\n\ngrBookList = ", str(grBookList).strip('[]'))
    #  print("\n\n1) randomList = ", str(randomList).strip('[]'))
    
    displayList = randomList[0:10]
    # print("\n\n2) displayList = ", str(displayList).strip('[]'))
    

    allBooks = []
    for bookID in displayList:
       book = grLookupByID(bookID)
       allBooks.append(book)
    #print("\n\nallBooks = ",allBooks)
    #for book in allBooks:
    #    print("\n\nbook = ",book)

    return render_template("homepage.html",
                            allBooks=allBooks
                            )
    

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    # Either if request.method == "POST" OR form.validate_on_submit(): works
    # The form.validate_on_submit() method does all the form processing work.
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
    
    # if request.method == "POST":
    
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    # """Register user"""
    # https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/
    
    form = RegisterForm()

    # Either if request.method == "POST" OR form.validate_on_submit(): works
    # The form.validate_on_submit() method does all the form processing work.
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
    
    # if request.method == "POST":

    if form.validate_on_submit():
        flash('Register requested for user {}, firstName={}, lastName={}'.format(
            form.username.data, form.firstName.data, form.lastName.data))
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route("/Search", methods=["GET", "POST"])
@app.route("/search", methods=["GET", "POST"])
def search():
    # """Search for books""
    return "Search for books"
    
@app.route("/review", methods=["GET", "POST"])
def review():
    # """Review a Book""
    return "Review a Book"
    
@app.route("/importBooks", methods=["GET", "POST"])
def importBooks():
    conString =  os.getenv("DATABASE_URL")

    try:
        connection = psycopg2.connect(conString)
        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")

        with open('books.txt', 'r') as f:
            # Notice that we don't need the 'txt' module.
            next(f) # Skip the header row.
            cursor.copy_from(f, 'books', columns=['isbn','title','author','year'])


    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):

                cursor.close()
                connection.commit()
                connection.close()
                print("PostgreSQL connection is closed")
                return "There was an error importing Books."

    return "Books have been successfully imported!"

