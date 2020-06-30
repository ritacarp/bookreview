from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db, grBookList
from app.models import People, Book, BookReview
from app.main import bp
from app.main.helpers import grLookupByID
import math
from sqlalchemy import asc, desc

import psycopg2
import os
import random



@bp.route('/')
@bp.route('/index')

def index():
    imagesPerRow = 10
    bookList = []
    books  = Book.query.filter(Book.image_url != None).order_by(desc(Book.average_score)).limit(100).all()
    for book in books: 
        bookID = book.id
        bookList.append(bookID)
    randomList = bookList.copy()
    random.shuffle(randomList)
    print("\n\nbookList = ", str(bookList).strip('[]'))
    print("\n\n1) randomList = ", str(randomList).strip('[]'))
    displayList = randomList[0:imagesPerRow]
    print("\n\n2) displayList = ", str(displayList).strip('[]'))
    allBooks = Book.query.filter(Book.id.in_(displayList))
    
    for book in allBooks:
        averageScore = book.average_score
        if averageScore == 5.0:
            scorePercent = 100
            yellowStars = 5
            paritalYellowStars = 0
            clearStars = 0
        else:
            scorePercent =  ((averageScore / 5) * 100);
            yellowStars = math.floor(averageScore)
            paritalYellowStars = averageScore - yellowStars
            clearStars = 5 - (yellowStars + 1)
         
        book.scorePercent = scorePercent



    return render_template("homepage.html",
                            allBooks=allBooks,
                            imagesPerRow=imagesPerRow
                            )



@bp.route('/book/')
@bp.route('/book/<bookID>')
def book(bookID=""):
    if not bookID:
        flash('Book ID is required for to view a book')
        return redirect(url_for('main.index'))
                            
    book = Book.query.get(bookID)

    averageScore = book.average_score
    if averageScore == 5.0:
        scorePercent = 100
        yellowStars = 5
        paritalYellowStars = 0
        clearStars = 0
    else:
        scorePercent =  ((averageScore / 5) * 100);
        yellowStars = math.floor(averageScore)
        paritalYellowStars = averageScore - yellowStars
        clearStars = 5 - (yellowStars + 1)
         
    book.scorePercent = scorePercent
    book.f_scorePercent = f"{scorePercent:,.2f}"

    
    return render_template("book.html",
                            book=book)

    

@bp.route("/Search", methods=["GET", "POST"])
@bp.route("/search", methods=["GET", "POST"])
def search():
    # """Search for books""
    return "Search for books"
    
@bp.route("/review", methods=["GET", "POST"])
def review():
    # """Review a Book""
    return "Review a Book"
    

