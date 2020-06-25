import os
import requests
import urllib.parse
# import xml.etree.ElementTree as ET
from app.models import Book
import math
from app.main.helpers import grLookupByID


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


def grLookupIDByISBN():
    # https://flask-bookreviews.herokuapp.com/launchTask/grLookupIDByISBN
    print("Starting task grLookupIDByISBN()")
    
    # These 2 lines are for testing:  Replace with the real filter
    filter = "%grish%"
    books = Book.query.filter( Book.author.ilike(filter)).all()
    
    totalCount = len(books)
    interval = math.floor(len(books) / 10)
    
    count = 0
    successCount = 0
    failCount = 0
    for book in books:
        count += 1
        
        grBookID = grLookupByISBN(book.isbn)
        
        # Update the book record with the grBookID
        if grBookID:
            successCount += 1
            book.grBookID = grBookID
            db.session.commit()
            print(f"Hurray!!  Updated GR Book ID {grBookID} from ISBN {book.isbn} !!")
        else:
            failCount += 1
            print(f"Boo There was no record of ISBN  {book.isbn} in the goodreads database")

        if count % interval == 0:
            print(f"\n\ngrLookupIDByISBN {count}: Found Book ID {grBookID} for ISBN {book.isbn})")

    print("\n\nTask grLookupIDByISBN() Finished Successfully!")
    print(f"Success Count = {successCount}; Fail Count = {failCount}; Total Count = {totalCount}\n\n")


def foo(start=0, end=10):
    i=0
    for x in range(start, end):
        i += 1
        print("In test worker:  x = ", x)
    return(i)
