import os
import requests
import urllib.parse
# import xml.etree.ElementTree as ET
from app.models import Book
import math
from app.main.helpers import grLookupByID, googleLookupByISBN
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
    # 127.0.0.1/tasks/test_updateBooksGRID
    # https://flask-bookreviews.herokuapp.com/tasks/launchTask/task_grUpdateIDByISBN
    
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
        
        #grBookID = grLookupByISBN(book.isbn)
        goodreadsBookID = grLookupByISBN(book.isbn)
        
        # Update the book record with the grBookID
        if goodreadsBookID:
            successCount += 1
            #book.gr_bookid = grBookID
            book.set_gr_bookid(goodreadsBookID)
            db.session.commit()
            # print(f"Hurray!!  Updated GR Book ID {book.gr_bookid} from ISBN {book.isbn} !!")
        else:
            failCount += 1
            # print(f"Boo There was no record of ISBN  {book.isbn} in the goodreads database")

        if count % interval == 0:
            print(f"\n\ngrUpdateIDByISBN {count}: Processing goodreads Book ID {goodreadsBookID})")

    print("\n\nTask grUpdateIDByISBN() Finished Successfully!")
    print(f"Success Count = {successCount}; Fail Count = {failCount}; Total Count = {totalCount}\n\n")


def booksUpdateByGRID():
    # 127.0.0.1/tasks/test_BooksUpdateByGRID
    # https://flask-bookreviews.herokuapp.com/tasks/launchTask/task_updateBooksByGRID
    
    # These 2 lines are for testing:  Replace with the real filter
    # filter = "%grish%"
    # books = Book.query.filter( and_(Book.author.ilike(filter), Book.gr_bookid != None)  ).all()
    
    #books = Book.query.filter(Book.gr_bookid != None).all()
    
    books = Book.query.filter(Book.image_url == None).all()
    
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
            goodreadsBook = grLookupByID(book.gr_bookid)
            #print(f"\n\nbooksUpdateByGRID():  goodreads book = {goodreadsBook}")
            
            book.set_review_count(goodreadsBook["review_count"])
            book.set_ratings_count(goodreadsBook["ratings_count"])
            book.set_average_score(goodreadsBook["average_score"])
            book.set_asin(goodreadsBook["asin"])
            book.set_kindle_asin(goodreadsBook["kindle_asin"])
            book.set_isbn13(goodreadsBook["isbn13"])
            book.set_stars_1(goodreadsBook["stars_1"])
            book.set_stars_2(goodreadsBook["stars_2"])
            book.set_stars_3(goodreadsBook["stars_3"])
            book.set_stars_4(goodreadsBook["stars_4"])
            book.set_stars_5(goodreadsBook["stars_5"])
            book.set_description(goodreadsBook["description"])
            book.set_image_url(goodreadsBook["image_url"])
            book.set_thumbnail_url(goodreadsBook["thumbnail_url"])
            book.set_amazon_lookup_id(goodreadsBook["amazon_lookup_id"])
            db.session.commit()
            successCount += 1
        except:
            failCount += 1

        if count % interval == 0:
            print(f"\n\nbooksUpdateByGRID() {count}: Processing Book ID ({book.gr_bookid})")

    print("\n\nTask nbooksUpdateByGRID() Finished Successfully!")
    print(f"Success Count = {successCount}; Fail Count = {failCount}; Total Count = {totalCount}\n\n")



def booksGoogleUpdateByISBN():
    # 127.0.0.1/tasks/test_booksGoogleUpdateByISBN
    # https://flask-bookreviews.herokuapp.com/tasks/launchTask/task_booksGoogleUpdateByISBN

    #books = Book.query.filter(Book.image_url == 'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png').all()
    books = Book.query.filter(Book.google_image_url != None).all()

    try:
       totalCount = len(books)
    except:
       totalCount = 0


    print(f"booksGoogleUpdateByISBN():  There are {totalCount} records in the books result set")
    if totalCount == 0:
        return

    interval = math.ceil(len(books) / 50)

    count = 0
    successCount = 0
    failCount = 0
    for book in books:
        count += 1
        #print(f"\n\n{book}")
        #print(f"booksGoogleUpdateByISBN(): the book id is {book.id}; the isbn is {book.isbn}")
        try:
            google_image_url = googleLookupByISBN(book.isbn)
            if google_image_url:
                #print(f"the google image url is {google_image_url}")
                book.set_google_image_url(google_image_url)
                book.set_homepage_image_url(google_image_url)
                db.session.commit()
                successCount += 1
            else:
                failCount += 1
            
        except:
            failCount += 1
            #print(f"There was an error getting google image url")
            #image_url = None

        if count % interval == 0:
            print(f"\n\booksGoogleUpdateByISBN() {count}: Processing Book ID ({book.gr_bookid})")

    print("\n\nTask nbooksGoogleUpdateByISBN() Finished Successfully!")
    print(f"Success Count = {successCount}; Fail Count = {failCount}; Total Count = {totalCount}\n\n")



    

    
     








def foo(start=0, end=10):
    i=0
    for x in range(start, end):
        i += 1
        print("In test worker:  x = ", x)
    return(i)
