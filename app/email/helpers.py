from flask_mail import Message
from app import mail
from flask import current_app, render_template

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



from app.models import People

#import sendgrid
#import os
#from sendgrid.helpers.mail import *

def send_password_reset_email(emailAddress):
    print(f"\n\n1)  send_password_reset_email:  emailAddress = {emailAddress}")
    print(f"\n\n2)  send_password_reset_email:  email server =  {os.environ.get('MAIL_SERVER')}")
    
    user = People.query.filter_by(email=emailAddress).first()
    token = user.get_reset_password_token()
    server = os.environ.get('SERVER')
    if server == "localhost":
        gmail_send_email('[Book Review] Reset Your Password',
                    sender=(os.environ.get('ADMINS')),
                    recipients=emailAddress,
                    text_body=render_template('email/email_reset_password.txt',username=user.username, token=token),
                    html_body=render_template('email/email_reset_password.html',username=user.username, token=token)
                   )
    else:
        # was send_sengrid_email
        # MAIL_SERVER=smtp.sendgrid.net
        # MAIL_USERNAME=apikey
        # MAIL_PASSWORD=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
        # ADMINS=flask.bookreviews@gmail.com
        # was send_sengrid_email
        
        gmail_send_email('subject=[Book Review] Reset Your Password',
                            sender=(os.environ.get('ADMINS')),
                            recipients=emailAddress,
                            text_body=render_template('email/email_reset_password.txt',username=user.username, token=token),
                            html_body=render_template('email/email_reset_password.html',username=user.username, token=token)
                   )



def gmail_send_email(subject, sender, recipients, text_body, html_body):
    port = os.environ.get('MAIL_PORT')  # For starttls
    smtp_server = os.environ.get('MAIL_SERVER')
    
    sender_email = os.environ.get('MAIL_USERNAME')
    password = os.environ.get('MAIL_PASSWORD')

    receiver_email = recipients
    
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    part1 = MIMEText(text_body, "plain")
    part2 = MIMEText(html_body, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    connection = smtplib.SMTP(smtp_server, port)
    connection.starttls(context=context)
    connection.login(sender_email, password)
    connection.sendmail(sender_email, receiver_email, message.as_string())


    
   

def send_email(subject, sender, recipients, text_body, html_body):
    print(f"\n\n3)  send_password_reset_email:  emailAddress = {recipients}")
    print(f"\n\n4)  send_password_reset_email:  email server =  {os.environ.get('MAIL_SERVER')}")

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
# https://sendgrid.com/docs/for-developers/sending-email/getting-started-smtp/#before-you-begin

# https://app.sendgrid.com/guide/integrate/langs/smtp

# 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

def send_sengrid_email(subject, sender, recipients, text_body, html_body):
    print(f"\n\n5)  send_password_reset_email:  emailAddress = {recipients}")
    print(f"\n\n6)  send_password_reset_email:  email server =  {os.environ.get('MAIL_SERVER')}")

    message = Mail(
        from_email=sender,
        to_emails=recipients,
        subject=subject,
        plain_text_content=text_body, 
        html_content=html_body)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"\n\n1) response.status_code = {response.status_code}")
        print(f"2) response.body = {response.body}")
        print(f"3) response.headers = {response.headers}")

    except Exception as e:
        print("5) in send_sengrid_email except - this is 5")
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