from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

print("Secret Key = ", app.config['SECRET_KEY'])
print("Database URL = ", app.config['SQLALCHEMY_DATABASE_URI'])

from app import routes, models