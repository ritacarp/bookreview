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
        #print(f"The response is {response.content}")
        grBookID = str(response.content, 'utf-8')
        return grBookID
        
        #print(f"Calling grLookupByID with grBookID = {grBookID}")
        #book = grLookupByID(grBookID)
        #print(f"\n\n grLookupByISBN:  UPDATE DATABASE HERE WITH BOOK = {book}")
        #return None
    except (KeyError, TypeError, ValueError):
        print(f"There was an exception raised in function grLookupByISBN({grISBN}) trying to read the response \n\n")
        return None


def goodreadsLookup():
    # https://flask-bookreviews.herokuapp.com/launchTask/goodreadsLookup
    print("Starting task goodreadsLookup()")
    filter = "%grish%"
    books = Book.query.filter( Book.author.ilike(filter)).all()
    interval = math.floor(len(books) / 10)
    
    count = 0
    for book in books:
        count += 1
        grBookID = grLookupByISBN(book.isbn)
        if count % interval == 0:
            print(f"\n\ngoodreadsLookup {count}: Found Book ID {grBookID} for ISBN {book.isbn})")

    print("Task goodreadsLookup() Finished Successfully!")


def foo(start=0, end=10):
    i=0
    for x in range(start, end):
        i += 1
        print("In test worker:  x = ", x)
    return(i)
