from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.models import People, Book, BookReview
from app.tasks import bp
# from app.main.helpers import grLookupByID
from app.tasks.helpers import grLookupIDByISBN
import math

import psycopg2
import os
import random


@bp.route("/launchTask", methods=["GET", "POST"])
@bp.route("/launchTask/<taskName>", methods=["GET", "POST"])
@bp.route("/launchTask/<taskName>/<args>", methods=["GET", "POST"])

def launchTask(taskName="", args=""):
    # https://python-rq.org/
    if taskName:
        if args:
            current_app.task_queue.enqueue('app.tasks.tasks.' + taskName, args, job_timeout='1h')
            return f"Task {taskName} has been successfully submitted with arguments {args}!"
        else:
            current_app.task_queue.enqueue('app.tasks.tasks.' + taskName)
            return f"Task {taskName} has been successfully submitted!"
    else:
        return "Please provide a task name (/launchTask/<taskName>/)"





@bp.route("/testLower", methods=["GET", "POST"])
def testLower():
    filter = "%grish%"
    print(f"testLower: filter is {filter}")
    books = Book.query.filter( Book.author.ilike(filter)).all()
    print(f"The number of books returned is {len(books)}")
    interval = math.floor(len(books) / 10)
    print(f"Interval = {interval}")
        
    count = 0
    for book in books:
        count += 1
        if count % interval == 0:
            print(f"testLower {count}:  Title: {book.title} ; Author: {book.author} ; ISBN: {book.isbn}")
    print(f"testLower: Done")
    return "testLower is done"


    
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

@bp.route("/updateBooks", methods=["GET", "POST"])
def updateBooks():
    print("updateBooks: started grLookupIDByISBN")
    grLookupIDByISBN()
    return "updateBooks: grLookupIDByISBN Finished Successfully!"