from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db, grBookList
from app.models import People, Book, BookReview
from app.main import bp
from app.main.helpers import grLookupByID
import math
from sqlalchemy import asc, desc,  and_, or_
from datetime import datetime

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
    # print("\n\nbookList = ", str(bookList).strip('[]'))
    # print("\n\n1) randomList = ", str(randomList).strip('[]'))
    displayList = randomList[0:imagesPerRow]
    # print("\n\n2) displayList = ", str(displayList).strip('[]'))
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



@bp.route('/book', methods=["GET", "POST"])
@bp.route('/book/<bookID>', methods=["GET", "POST"])
def book(bookID=""):
    if request.method == "GET":
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

        allBookReviews = BookReview.query.filter(BookReview.book_id==bookID).order_by(BookReview.review_date.desc()).all()
        countBookReviews = BookReview.query.filter(BookReview.book_id==bookID).count()
    
        return render_template("book.html",
                                book=book,
                                bookID=bookID,
                                allBookReviews=allBookReviews,
                                countBookReviews=countBookReviews,
                                loginNext=f"?next=/book/{bookID}")

    review = request.form.get("review")
    
    review = f"<p style='white-space: pre-line'>{review}</p>"
    score = request.form.get("score")
    userName = current_user.username
    userID = current_user.id
    bookID = request.form.get("bookID")
    
    book_review = BookReview.query.filter( and_(  BookReview.people_id==userID, BookReview.book_id==bookID  )  ).first()
    if book_review is None:
        print(f'book review not found for book id {bookID}, person {userName};  inserting book')
        book_review = BookReview(people_id=userID, book_id=bookID, review=review, score=score, review_date=datetime.utcnow())
        db.session.add(book_review)
    else:
        book_review.set_review(review)
        book_review.set_score(score)
        book_review.set_review_date(datetime.utcnow())
    db.session.commit()

    
    ##return f"Thank you, {userName} / {userID}  for your review of book {bookID} {review}"
    flash(f"Thank you, {userName} / {userID} for your review of {score} stars for book {bookID} {review}", "success")
    return redirect(url_for('main.index'))


    

@bp.route("/Search", methods=["GET", "POST"])
@bp.route("/search", methods=["GET", "POST"])
def search():
    # """Search for books""
    return "Search for books"
    

#@bp.route("/review", methods=["GET", "POST"])
#@login_required
#def review():
#    # """Review a Book""
    
#    #flash("This is message 1.<br>This is message 2.<br>This is message 3.", "success")  
#    if request.method == "GET":
#       return render_template("review.html")
    
#    review = request.form.get("review")
    
#    review = f"<p style='white-space: pre-line'>{review}</p>"
#    score = request.form.get("score")
#    userName = current_user.username
#    userID = current_user.id
#    bookID = request.form.get("bookID")
#    ##return f"Thank you, {userName} / {userID}  for your review of book {bookID} {review}"
#    flash(f"Thank you, {userName} / {userID} for your review of {score} stars for book {bookID} {review}", "success")
#    return redirect(url_for('main.index'))

