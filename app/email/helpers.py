from flask_mail import Message
from app import mail
from flask import current_app, render_template

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Book Review] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/email_reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/email_reset_password.html',
                                         user=user, token=token))


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)