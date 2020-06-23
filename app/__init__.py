import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import Config

from redis import Redis
import rq

# from rq import Queue
# from rq.job import Job
# from worker import conn

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()

grBookList = [3,2767052,2657,5907,5,6,1885,136251,5470,15881,7613,34,6148028,4671,48855,100915,7624,5107,968,77203,2429135,13496,11870085,10210,18135,17470674,19063,930,4667024,1934,3636,960,386162,18619684,5129,21480930,24178,157993,6185,2956,18405,33574273,10917]


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # This comment ties the database with the Flask application
    # I think you can also write it as db = SQLAlchemy(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)


    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    
    print("create_app:  Secret Key = ", app.config['SECRET_KEY'])
    print("create_app:  Database URL = ", app.config['SQLALCHEMY_DATABASE_URI'])


    return app





# q = Queue(connection=conn)


from app import models