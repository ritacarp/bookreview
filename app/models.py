from datetime import datetime
from time import time
from app import db, login
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import force_instant_defaults
from hashlib import md5
import jwt



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


class People(UserMixin, db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    hash = db.Column(db.String, nullable=True)
    comments = db.Column(db.String, nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    bookReviews = db.relationship('BookReview', backref='reviewer', lazy=True)

    def __repr__(self):
        return '<Person: User Name: {}, Email: {}, hash: {}, comments: {}>'.format(self.username, self.email, self.hash, self.comments)    

    def set_password(self, password):
        self.hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://s.gravatar.com/avatar/{digest}?s={size}&d=blank'
        
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')


    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return People.query.get(id)



@login.user_loader
def load_user(id):
    return People.query.get(int(id))


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
    gr_bookid = db.Column(db.String, nullable=True)
    asin = db.Column(db.String, nullable=True)
    kindle_asin = db.Column(db.String, nullable=True)
    isbn13 = db.Column(db.String, nullable=True)
    stars_1 = db.Column(db.Integer, nullable=True)
    stars_2 = db.Column(db.Integer, nullable=True)
    stars_3 = db.Column(db.Integer, nullable=True)
    stars_4 = db.Column(db.Integer, nullable=True) 
    stars_5 = db.Column(db.Integer, nullable=True) 
    image_url = db.Column(db.String, nullable=True)
    thumbnail_url = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    amazon_lookup_id = db.Column(db.String, nullable=True)
    google_image_url = db.Column(db.String, nullable=True)
    homepage_image_url = db.Column(db.String, nullable=True)
    bookReviews = db.relationship('BookReview', backref='book', lazy=True)
    def __repr__(self):
        return '<Book: ISBN: {}, Title: {}, Author: {}, Year: {}>'.format(self.isbn, self.title, self.author, self.year)    

    def set_isbn(self, isbn):
        self.isbn = isbn

    def set_title(self, title):
        self.title = title

    def set_author(self, author):
        self.author = author

    def set_year(self, year):
        self.year = year

    def set_review_count(self, review_count):
        try:
            self.review_count = int(review_count)
        except:
            self.review_count = 0

    def set_ratings_count(self, ratings_count):
        try:
            self.ratings_count = int(ratings_count)
        except:
            self.ratings_count = 0

    def set_average_score(self, average_score):
        try:
            self.average_score = float(average_score)
        except:
            self.average_score = 0

    def set_gr_bookid(self, gr_bookid):
        self.gr_bookid = gr_bookid

    def set_asin(self, asin):
        self.asin = asin

    def set_kindle_asin(self, kindle_asin):
        self.kindle_asin = kindle_asin

    def set_isbn13(self, isbn13):
        self.isbn13 = isbn13

    def set_stars_1(self, stars_1):
        try:
            self.stars_1 = int(stars_1)
        except:
             self.stars_1 = 0

    def set_stars_2(self, stars_2):
        try:
            self.stars_2 = int(stars_2)
        except:
             self.stars_2 = 0

    def set_stars_3(self, stars_3):
        try:
            self.stars_3 = int(stars_3)
        except:
             self.stars_3 = 0

    def set_stars_4(self, stars_4):
        try:
            self.stars_4 = int(stars_4)
        except:
             self.stars_4 = 0

    def set_stars_5(self, stars_5):
        try:
            self.stars_5 = int(stars_5)
        except:
             self.stars_5 = 0

    def set_image_url(self, image_url):
        self.image_url = image_url

    def set_thumbnail_url(self, thumbnail_url):
        self.thumbnail_url = thumbnail_url

    def set_description(self, description):
        self.description = description

    def set_amazon_lookup_id(self, amazon_lookup_id):
        self.amazon_lookup_id = amazon_lookup_id

    def set_google_image_url(self, google_image_url):
        self.google_image_url = google_image_url

    def set_homepage_image_url(self, homepage_image_url):
        self.homepage_image_url = homepage_image_url

 
class BookReview(db.Model):
    __tablename__ = "book_reviews"
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'),  nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    review = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    review_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
 
    def set_score(self, score):
        try:
            self.score = int(score)
        except:
            self.score = 0

    def set_review(self, review):
        self.review = review

    def set_review_date(self, review_date):
        try:
            self.review_date = review_date
        except:
            self.review_date = datetime.utcnow()

