from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user
from app import db
from app.email import bp
from app.email.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.email.helpers import send_password_reset_email, send_email


from app.models import People

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user:
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = People.query.filter_by(email=form.email.data).first()
        if user:
            #send_password_reset_email(user)
            send_password_reset_email(user.email)
            print(f"email route reset_password_request():  user.email = {user.email}")
        flash('Check your email for the instructions to reset your password',"information")
        return redirect(url_for('auth.login'))
    return render_template('email/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):

    if current_user:
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
    
    person = People.verify_reset_password_token(token)
    if not person:
        return redirect(url_for('main.index'))
        
    form = ResetPasswordForm()
    if form.validate_on_submit():
        person.comments=form.password.data
        person.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.',"success")
        return redirect(url_for('auth.login'))
    
    
    return render_template('email/reset_password.html',
                           title='Reset Password', form=form)
