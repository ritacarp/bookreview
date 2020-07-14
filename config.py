import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    GOODREADS_PUBLIC_KEY = os.environ.get('GOODREADS_PUBLIC_KEY')
    REDIS_URL = os.environ.get('REDIS_URL')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS')
    SENDGRID_API_KEY=os.environ.get('SENDGRID_API_KEY')
    SENDGRID_USERNAME=os.environ.get('SENDGRID_USERNAME')
    SENDGRID_PASSWORD=os.environ.get('SENDGRID_PASSWORD')
    SERVER=os.environ.get('SERVER')