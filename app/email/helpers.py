from flask_mail import Message
from app import mail
from flask import current_app, render_template

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

#import sendgrid
#import os
#from sendgrid.helpers.mail import *

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    server = os.environ.get('SERVER')
    if server == "localhost":
        send_email('[Book Review] Reset Your Password',
                    sender=current_app.config['ADMINS'][0],
                    recipients=[user.email],
                    text_body=render_template('email/email_reset_password.txt',user=user, token=token),
                    html_body=render_template('email/email_reset_password.html',user=user, token=token)
                   )
    else:
        send_sengrid_email('subject=[Book Review] Reset Your Password',
                            sender=os.environ.get('ADMINS'),
                            recipients=[user.email],
                            text_body=render_template('email/email_reset_password.txt',user=user, token=token),
                            html_body=render_template('email/email_reset_password.html',user=user, token=token)
                   )
   

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


# Original key - does not work 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
# New Key - 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
#  https://app.sendgrid.com/account/details
# https://app.sendgrid.com/settings/api_keys
# https://devcenter.heroku.com/articles/sendgrid#python
# https://devcenter.heroku.com/articles/sendgrid#setup-api-key-environment-variable

# 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

def send_sengrid_email(subject, sender, recipients, text_body, html_body):
    print("\n\n1) in send_sengrid_email - this is 1")
    message = Mail(
        from_email=sender,
        to_emails=recipients,
        subject=subject,
        plain_text_content=text_body, 
        html_content=html_body)
    print("2) in send_sengrid_email - this is 2")
    try:
        print("3) in send_sengrid_email try - this is 3")
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        print("4) in send_sengrid_email try - this is 4")
        response = sg.send(message)
        print("5) in send_sengrid_email try - this is 5")
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("6) in send_sengrid_email except - this is 6")
        print(e.message)


def x_send_sengrid_email(subject, sender, recipients, text_body, html_body):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = sender
    to_emails = recipients
    subject = subject
    plain_text_content=text_body
    html_content = html_body
    #mail = Mail(from_email, subject, to_email, content)
    
    
    mail = sendgrid.helpers.mail.Mail(
                                      from_email=sender, 
                                      to_emails=recipients,  
                                      subject=subject, 
                                      plain_text_content=text_body,  
                                      html_content=html_body)
    
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)