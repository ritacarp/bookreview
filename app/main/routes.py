from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db, grBookList
from app.models import People, Book, BookReview
from app.main import bp
from app.main.helpers import grLookupByID
import math

import psycopg2
import os
import random

@bp.route('/')
@bp.route('/index')

def index():

    # http://www.datasciencemadesimple.com/strip-lstriprstrip-strip-function-python/
    # To strip off leading zeros - I googled python strip leading zeros
    
    # To shuffle a list
    # https://note.nkmk.me/en/python-random-shuffle/
    
    randomList = grBookList.copy()
    random.shuffle(randomList)
    # print("\n\ngrBookList = ", str(grBookList).strip('[]'))
    #  print("\n\n1) randomList = ", str(randomList).strip('[]'))
    
    displayList = randomList[0:10]
    # print("\n\n2) displayList = ", str(displayList).strip('[]'))
    

    allBooks = []
    
    idx = -1
    bookCount = 0
    loopCount = 0
    imagesPerRow = 9
    maxLoops = len(randomList)
    while True:

        loopCount += 1
        if loopCount > maxLoops:
            break

        idx += 1
        # print("idx = ", idx, "Loop Count = ", loopCount)

        grBookID = randomList[idx]
        book = grLookupByID(grBookID)
        if book["amazon_lookup_id"]:
           allBooks.append(book)
           bookCount += 1
           if bookCount == imagesPerRow:
               break

        # print("Book Count = ", bookCount)

    
    return render_template("homepage.html",
                            allBooks=allBooks,
                            imagesPerRow=imagesPerRow
                            )
    

    

@bp.route("/Search", methods=["GET", "POST"])
@bp.route("/search", methods=["GET", "POST"])
def search():
    # """Search for books""
    return "Search for books"
    
@bp.route("/review", methods=["GET", "POST"])
def review():
    # """Review a Book""
    return "Review a Book"
    

