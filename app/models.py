from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    hash = db.Column(db.String, nullable=False)
    comments = db.Column(db.String, nullable=False)
    bookReviews = db.relationship('BookReview', backref='people', lazy=True)

    def __repr__(self):
        return '<Person: User Name: {}, Email: {}, hash: {}, comments: {}>'.format(self.username, self.email, self.hash, self.comments)    


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(80), unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    review_count = db.Column(db.Integer, nullable=False, default=0)
    average_score = db.Column(db.Float, nullable=False, default=0)
    bookReviews = db.relationship('BookReview', backref='books', lazy=True)

 
class BookReview(db.Model):
    __tablename__ = "book_reviews"
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'),  nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    review = db.Column(db.String, nullable=False)
 
 


