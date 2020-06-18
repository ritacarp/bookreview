from flask import render_template, flash, redirect, request, url_for
from app import app
from app.forms import LoginForm

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
    return "In Register"


@app.route("/Search", methods=["GET", "POST"])
@app.route("/search", methods=["GET", "POST"])
def search():
    # """Search for books""
    return "Search for books"
    
@app.route("/review", methods=["GET", "POST"])
def review():
    # """Review a Book""
    return "Review a Book"


