from flask import render_template, flash, redirect, request, url_for
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user

from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm
from app.models import People


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    
    # Either if request.method == "POST" OR form.validate_on_submit(): works
    # The form.validate_on_submit() method does all the form processing work.
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
    
    # if request.method == "POST":
    
    if form.validate_on_submit():
        user = People.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))

        # These next 3 lines are for testing
        # flash('Login requested for user {}, remember_me={}'.format(
        #     form.username.data, form.remember_me.data))
        # return redirect(url_for('main.index'))

        login_user(user, remember=form.remember_me.data)        
        next_page = request.args.get('next')
        
        # For testing
        if next_page:
           print(f"next_page = {next_page};  url_parse(next_page).netloc = {url_parse(next_page).netloc}")
        
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)


        
    return render_template('auth/login.html', title='Sign In', form=form)



@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@bp.route("/register", methods=["GET", "POST"])
def register():
    # """Register user"""
    # https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/
    
    form = RegisterForm()

    # Either if request.method == "POST" OR form.validate_on_submit(): works
    # The form.validate_on_submit() method does all the form processing work.
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
    
    # if request.method == "POST":

    if form.validate_on_submit():
        user = Person(username=form.username.data, email=form.email.data, comments=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        #flash('Register requested for user {}, firstName={}, lastName={}'.format(
        #    form.username.data, form.firstName.data, form.lastName.data))
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


