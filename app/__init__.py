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


# Most Flask extensions are initialized by creating an instance of the extension and passing the application as an argument
# Example:  db = SQLAlchemy(app)
# But when initializing Blueprints, we have a lot of little apps
# There is not a global app
#
# Therefore, we create an instance of each flask extension in the global scope as before, but no arguments are passed to it.
# Example:  
#          db = SQLAlchemy() - see below
# Then, we have a function called create_app, which is an application factory function
# The first line in the function creates the Flask application, and the second line reads the config variables
# And then we can tie the extension instances to application by calling the method init_app to bind the extension to the
#      application that we just created
# Example:  
#          db.init_app(app) - Remember, we created db in the global scope, and here we are binding it to the application
#
# Who calls the application factory function?
# The module that starts the application:  in this case bookreview.py which we defined in environment variable FLASK_APP 
# The top-level bookreview.py script, which is the only module in which the application now exists in the global scope.


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
    
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('flask-bookreviews-tasks', connection=app.redis)


    
    print("create_app:  Secret Key = ", app.config['SECRET_KEY'])
    print("create_app:  Database URL = ", app.config['SQLALCHEMY_DATABASE_URI'])


    return app





# q = Queue(connection=conn)


from app import models