import os
import requests
import urllib.parse
# import xml.etree.ElementTree as ET
from app.models import Book
import math
from app.main.helpers import grLookupByID
from app import db
from app.main.helpers import grLookupByID
from sqlalchemy import and_, or_


def grLookupByISBN(grISBN):
    """Look up quote for symbol."""
    # https://docs.python.org/3.4/library/xml.etree.elementtree.html

    # Contact API
    try:
        api_key = os.environ.get("GOODREADS_PUBLIC_KEY")
        response = requests.get(f"https://www.goodreads.com/book/isbn_to_id/{grISBN}?key={api_key}") 
        response.raise_for_status()
    except requests.RequestException:        
        print(f"There was an exception raised in function grLookupByISBN({grISBN}) \n\n")
        return None
        
    try:  
        grBookID = str(response.content, 'utf-8')
        return grBookID
        
    except (KeyError, TypeError, ValueError):
        print(f"There was an exception raised in function grLookupByISBN({grISBN}) trying to read the response \n\n")
        return None


def grUpdateIDByISBN():
    # https://flask-bookreviews.herokuapp.com/launchTask/grUpdateIDByISBN
    print("Starting task grUpdateIDByISBN()")
    
    # These 2 lines are for testing:  Replace with the real filter
    # filter = "%grish%"
    # books = Book.query.filter( Book.author.ilike(filter)).all()
    
    books = Book.query.filter(Book.gr_bookid == None).all()

    try:
       totalCount = len(books)
    except:
       totalCount = 0
    
    print(f"gr_bookid == None:  There are {totalCount} records in the books result set")
    if totalCount == 0:
        return

       
    interval = math.ceil(len(books) / 50)
    
    count = 0
    successCount = 0
    failCount = 0
    for book in books:
        count += 1
        
        grBookID = grLookupByISBN(book.isbn)
        
        # Update the book record with the grBookID
        if grBookID:
            successCount += 1
            book.gr_bookid = grBookID
            db.session.commit()
            # print(f"Hurray!!  Updated GR Book ID {book.gr_bookid} from ISBN {book.isbn} !!")
        else:
            failCount += 1
            # print(f"Boo There was no record of ISBN  {book.isbn} in the goodreads database")

        if count % interval == 0:
            print(f"\n\ngrUpdateIDByISBN {count}: Processing Book ID {grBookID})")

    print("\n\nTask grUpdateIDByISBN() Finished Successfully!")
    print(f"Success Count = {successCount}; Fail Count = {failCount}; Total Count = {totalCount}\n\n")


def booksUpdateByGRID():
    # These 2 lines are for testing:  Replace with the real filter
    filter = "%grish%"
    books = Book.query.filter( and_(Book.author.ilike(filter), Book.gr_bookid != None)  ).all()
    
    try:
       totalCount = len(books)
    except:
       totalCount = 0
    
    print(f"booksUpdateByGRID():  There are {totalCount} records in the books result set")
    if totalCount == 0:
        return

       
    interval = math.ceil(len(books) / 50)
    
    count = 0
    successCount = 0
    failCount = 0
    for book in books:
        count += 1
        try:
            grBook = grLookupByID(book.gr_bookid)
            # print(f"\n\nbooksUpdateByGRID():  book = {grBook}")
            thisBook = Book.query.get(book.id)
            print(f"\n\n RITA  booksUpdateByGRID():  book to update = {thisBook}")
            thisBook.description = grBook.description
            thisBook.image_url = grBook.image_url
            thisBook.thumbnail_url = grBook.thumbnail_url
            db.session.commit()
            successCount += 1
        except:
            failCount += 1

        if count % interval == 0:
            print(f"\n\nbooksUpdateByGRID() {count}: Processing Book ID ({book.gr_bookid})")

    print("\n\nTask nbooksUpdateByGRID() Finished Successfully!")
    print(f"Success Count = {successCount}; Fail Count = {failCount}; Total Count = {totalCount}\n\n")



def foo(start=0, end=10):
    i=0
    for x in range(start, end):
        i += 1
        print("In test worker:  x = ", x)
    return(i)
