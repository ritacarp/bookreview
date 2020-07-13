from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db, grBookList
from app.models import People, Book, BookReview
from app.main import bp
from app.main.helpers import grLookupByID, googleLookup
import math
from sqlalchemy import asc, desc,  and_, or_
from datetime import datetime
from app.main.forms import EditProfileForm

import psycopg2
import os
import random

@bp.before_request
def before_request():
    if current_user:
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()



@bp.route('/')
@bp.route('/index')

def index():
    page = request.args.get('page', 1, type=int)
    imagesPerRow = 9
    bookList = []

    
    allBooks  = Book.query.filter(Book.image_url != None).order_by(desc(Book.average_score)).paginate(page, int(imagesPerRow*2), False)
    bookCount = Book.query.filter(Book.image_url != None).count()
    lastPage = math.ceil(bookCount / (imagesPerRow*2))

    if allBooks.has_next:
        next_url = url_for('main.index', page=allBooks.next_num)
    else:
        next_url = None

    if allBooks.has_prev:
        prev_url  = url_for('main.index', page=allBooks.prev_num)
    else:
        prev_url  = None


    #books  = Book.query.filter(Book.image_url != None).order_by(desc(Book.average_score)).limit(100).all()
    #for book in books: 
    #    bookID = book.id
    #    bookList.append(bookID)
    #randomList = bookList.copy()
    #random.shuffle(randomList)
    # print("\n\nbookList = ", str(bookList).strip('[]'))
    # print("\n\n1) randomList = ", str(randomList).strip('[]'))
    #displayList = randomList[0:imagesPerRow]
    # print("\n\n2) displayList = ", str(displayList).strip('[]'))
    #allBooks = Book.query.filter(Book.id.in_(displayList))
    
    for book in allBooks.items:
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
                            allBooks=allBooks.items,
                            imagesPerRow=imagesPerRow,
                            next_url=next_url, prev_url=prev_url,
                            lastPage=str(lastPage)
                            )



@bp.route('/book', methods=["GET", "POST"])
@bp.route('/book/<bookID>', methods=["GET", "POST"])
def book(bookID=""):
    if request.method == "GET":
        if not bookID:
            flash('Book ID is required for to view a book')
            return redirect(url_for('main.index'))
                            
        book = Book.query.get(bookID)
        
        user_review = ""
        user_score = 0
        if current_user.is_authenticated:
           try:
               book_review = BookReview.query.filter( and_(  BookReview.people_id==current_user.id, BookReview.book_id==bookID  )  ).first()
               user_review=book_review.review
               user_score = book_review.score
           except:
               user_review = "" 
               user_score=0
        
        print(f"\n\n\nUser is authenticated = {current_user.is_authenticated}")
        print(f"user_review = {user_review}, user_score = {user_score}")

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
        #book.f_scorePercent = f"{scorePercent:,.2f}"

        allBookReviews = BookReview.query.filter(BookReview.book_id==bookID).order_by(BookReview.review_date.desc()).all()
        countBookReviews = BookReview.query.filter(BookReview.book_id==bookID).count()
    
        return render_template("book.html",
                                book=book,
                                bookID=bookID,
                                allBookReviews=allBookReviews,
                                countBookReviews=countBookReviews,
                                user_review=user_review,
                                user_score=user_score,
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
    
    print(f"\n\n\n6)in main.book, posting review for book {book_review.book.title}, id={bookID}")

    flash(f"Thank you, {userName} for your review", "success")
    return redirect(url_for('main.book', bookID=bookID))



    

@bp.route("/search", methods=["GET", "POST"])
@bp.route("/search/", methods=["GET", "POST"])
@bp.route("/search/<value>", methods=["GET", "POST"])
def search(value=""):
    # """Search for books""
    
    # select * from books 
    # Where id in (5007, 5004, 5008)
    # And (
    #       lower(title) like lower('%dear edward%')
    #       or 
    #       lower(author) like lower('%dear edward%') 
    #      )

    if value == "":
        flash(f"please enter a search value", "danger")  
        return redirect(url_for('main.index'))
        
    searchBook = googleLookup(value)
    print("\n\n")


    print(f"\n\nsearch:  isbns = {searchBook['isbns']}")
    print(f"\nsearch:  ids = {searchBook['bookIDs']}")
    
    resultCount = searchBook['count']


    print("\n\n")
    # return f"The number of values returned is {searchBook['count']}"
    

    page = request.args.get('page', 1, type=int)
    imagesPerRow = 9
    bookList = []

    lower_value = value.lower()
    filter = "%" + lower_value + "%"

    allBooks = Book.query.filter( and_(   Book.id.in_(searchBook['bookIDs']), (or_ ( Book.author.ilike(filter), Book.title.ilike(filter)))  )   ).paginate(page, int(imagesPerRow*2), False)
    bookCount = Book.query.filter( and_(   Book.id.in_(searchBook['bookIDs']), (or_ ( Book.author.ilike(filter), Book.title.ilike(filter)))  )   ).count()
    lastPage = math.ceil(bookCount / (imagesPerRow*2))

    if allBooks.has_next:
        next_url = url_for('main.index', page=allBooks.next_num)
    else:
        next_url = None

    if allBooks.has_prev:
        prev_url  = url_for('main.index', page=allBooks.prev_num)
    else:
        prev_url  = None

    for book in allBooks.items:
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

    if bookCount > 0:
        flash(f"There were {bookCount} results for search value {value} ", "success") 
        return render_template("homepage.html",
                                allBooks=allBooks.items,
                                imagesPerRow=imagesPerRow,
                                next_url=next_url, prev_url=prev_url,
                                lastPage=str(lastPage)
                                )
    else:
        flash(f"There were no results for search value  {value} ", "danger")  
        return redirect(url_for('main.index'))
     




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


@bp.route('/person')
@bp.route('/person/<username>')
def person(username = ""):

    if username == "":
        flash(f"username is required", "danger")  
        return redirect(url_for('main.index'))
    
    
    person = People.query.filter_by(username=username).first()
    if person is None:
        flash(f"user {username} does not exist", "danger")  
        return redirect(url_for('main.index'))
    
    fullName = person.first_name
    if fullName:
       fullName = fullName + " " + person.last_name
    allBookReviews = BookReview.query.filter(BookReview.people_id==person.id).order_by(BookReview.review_date.desc()).all()
    
    return render_template("person.html",
                            person=person,
                            fullName=fullName,
                            allBookReviews=allBookReviews)

        

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    print(f"\n\n1)  in main.edit_profile, method={request.method}")
    form = EditProfileForm()
    # if request.method == "POST":
    if form.validate_on_submit():
        print(f"2)  in main.edit_profile, in validate_on_submit method should be POST, methid is {request.method}")
        person = People.query.filter_by(username=current_user.username).first()
        if person is not None:
            person.email = form.email.data
            person.first_name = form.first_name.data
            person.last_name = form.last_name.data
            print(f"3)  in main.edit_profile, before commit")
            db.session.commit()
            print(f"4)  in main.edit_profile, after commit")
            flash("Your profile has been updated successfully","success")
            return redirect(url_for('main.person', username=person.username))
    
    
    person = People.query.filter_by(username=current_user.username).first()
    form.username.data = person.username
    form.email.data = person.email
    form.first_name.data = person.first_name
    form.last_name.data = person.last_name
    form.submit.label.text = 'Update Profile'

    return render_template('editProfile.html', title='Edit Profile', form=form)

@bp.route('/oauth2callback', methods=['GET', 'POST'])
@bp.route('/oauth2callback/<token>', methods=['GET', 'POST'])
def oauth2callback(token=""):
    print(f"the oauth2 callback token is {token}")
