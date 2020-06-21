from flask import render_template, flash, redirect, request, url_for
from app import app
from app.forms import LoginForm, RegisterForm

import os

@app.route('/<vTitle>/<vName>')
@app.route('/index/<vTitle>/<vName>')
@app.route('/')
@app.route('/index')

def index(vTitle="",vName=""):
    if not vTitle:
        title="Title for new uses"
    else:
        title=vTitle

    if not vName:
        user = {'username': 'All New Users'}
    else:
        user = {'username': vName}
        

    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]


    return render_template("index.html",
                               title=title,
                               user = user,
                               posts=posts
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



