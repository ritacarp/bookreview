from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db, grBookList
from app.models import People, Book, BookReview
from app.main import bp
from app.main.helpers import grLookupByID

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
        if book["bookID"]:
           allBooks.append(book)
           bookCount += 1
           if bookCount == imagesPerRow:
               break

        # print("Book Count = ", bookCount)
        
        
    
    #for bookID in displayList:
    #   book = grLookupByID(bookID)
    #  allBooks.append(book)
    #print("\n\nallBooks = ",allBooks)
    #for book in allBooks:
    #    print("\n\nbook = ",book)

    return render_template("homepage.html",
                            allBooks=allBooks,
                            imagesPerRow=imagesPerRow
                            )
    

    

@bp.route("/launchTask", methods=["GET", "POST"])
@bp.route("/launchTask/<taskName>", methods=["GET", "POST"])
@bp.route("/launchTask/<taskName>/<args>", methods=["GET", "POST"])

def launchTask(taskName="", args=""):
    # https://python-rq.org/
    if taskName:
        if args:
            current_app.task_queue.enqueue('app.tasks.' + taskName, args)
        else:
            current_app.task_queue.enqueue('app.tasks.' + taskName)
        return f"Task {taskName} has been successfully submitted!"
    else:
        return "Please provide a task name (/launchTask/<taskName>/)"




@bp.route("/Search", methods=["GET", "POST"])
@bp.route("/search", methods=["GET", "POST"])
def search():
    # """Search for books""
    return "Search for books"
    
@bp.route("/review", methods=["GET", "POST"])
def review():
    # """Review a Book""
    return "Review a Book"
    
@bp.route("/importBooks", methods=["GET", "POST"])
def importBooks():
    conString =  os.getenv("DATABASE_URL")

    try:
        connection = psycopg2.connect(conString)
        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")

        with open('books.txt', 'r') as f:
            # Notice that we don't need the 'txt' module.
            next(f) # Skip the header row.
            cursor.copy_from(f, 'books', columns=['isbn','title','author','year'])


    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):

                cursor.close()
                connection.commit()
                connection.close()
                print("PostgreSQL connection is closed")
                return "There was an error importing Books."

    return "Books have been successfully imported!"

