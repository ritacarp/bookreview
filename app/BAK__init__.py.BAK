from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from redis import Redis
import rq

# from rq import Queue
# from rq.job import Job
# from worker import conn

app = Flask(__name__)
app.config.from_object(Config)

# This comment ties the database with the Flask application
# I think you can also write it as db.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

grBookList = [3,2767052,2657,5907,5,6,1885,136251,5470,15881,7613,34,6148028,4671,48855,100915,7624,5107,968,77203,2429135,13496,11870085,10210,18135,17470674,19063,930,4667024,1934,3636,960,386162,18619684,5129,21480930,24178,157993,6185,2956,18405,33574273,10917]


# q = Queue(connection=conn)

print("Secret Key = ", app.config['SECRET_KEY'])
print("Database URL = ", app.config['SQLALCHEMY_DATABASE_URI'])

from app import routes, models