from datetime import datetime
from app import db
from sqlalchemy_utils import force_instant_defaults
from werkzeug.security import generate_password_hash, check_password_hash

#from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy()

# It is an unfortunate inconsistency that in some instances such as in a db.relationship() call, 
# the model is referenced by the model class, which typically starts with an uppercase character, 
# while in other cases such as this db.ForeignKey() declaration, a model is given by its database table name

# The first argument to db.relationship is the model class that represents the "many" side of the relationship.
# This argument can be provided as a string with the class name if the model is defined later in the module.

# The backref argument defines the name of a field that will be added to the objects (records) of the "many" class 
#     that points back at the "one" object.
# So here I am naming the backref in the People class to reviewer
# This will add a bookreview.reviewer expression that will return the reviewer of a given a book review.

# Take away:  db.relationship() call arguments are 1) Model Class Name 2) Table Name 3) lazy
#             db.ForeignKey('people.id'), or, more generally (TABLE_NAME.COLUMN_NAME)


class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=True)
    comments = db.Column(db.String, nullable=True)
    bookReviews = db.relationship('BookReview', backref='reviewer', lazy=True)

    def __repr__(self):
        return '<Person: User Name: {}, Email: {}, hash: {}, comments: {}>'.format(self.username, self.email, self.hash, self.comments)    

    def set_password(self, password):
        self.hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash, password)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    review_count = db.Column(db.Integer, nullable=True)
    ratings_count = db.Column(db.Integer, nullable=True)
    average_score = db.Column(db.Float, nullable=True)
    bookReviews = db.relationship('BookReview', backref='book', lazy=True)
    def __repr__(self):
        return '<Book: ISBN: {}, Title: {}, Author: {}, Year: {}>'.format(self.isbn, self.title, self.author, self.year)    

 
class BookReview(db.Model):
    __tablename__ = "book_reviews"
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'),  nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    review = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    review_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
 
 


