import os
import requests
import urllib.parse
import xml.etree.ElementTree as ET
from app.models import Book



def grLookupByID(grID):
    """Look up quote for symbol."""
    # https://docs.python.org/3.4/library/xml.etree.elementtree.html

    # Contact API
    try:
        api_key = os.environ.get("GOODREADS_PUBLIC_KEY")
        response = requests.get(f"https://www.goodreads.com/book/show/{grID}.xml?key={api_key}")  
        response.raise_for_status()
    except requests.RequestException:        
        return None

    
    try:
        root = ET.fromstring(response.content)
        
        #topLevelNodes = root.findall(".")
        #bookNodes = root.findall("./book")
        
        bookIDNode = root.findall("./book/id")
        grBookID = bookIDNode[0].text
        print("grBookID = ", grBookID)
        
        isbnNode = root.findall("./book/isbn")
        isbn = isbnNode[0].text
        if isbn:
            isbn.strip()
        print("isbn = ", isbn)
        
        asinNode = root.findall("./book/asin")
        asin = asinNode[0].text
        if asin:
            asin.strip()
        print("asin = ", asin)

        kindle_asinNode = root.findall("./book/kindle_asin")
        kindle_asin = kindle_asinNode[0].text
        if kindle_asin:
            kindle_asin.strip()
        print("kindle_asin = ", kindle_asin)
        
        bookID = asin
        if bookID is None or bookID == "":
            bookID = kindle_asin
        if bookID is None or bookID == "":
            bookID = isbn
        print("bookID = ", bookID)

        
        titleNode = root.findall("./book/title")
        title = titleNode[0].text
        # print("title = ", title)
        
        descriptionNode = root.findall("./book/description")
        description = "<h6><small>" + descriptionNode[0].text + "</small></h6>"
        # print("\n\ndescription = ", description)

        image_urlNode = root.findall("./book/image_url")
        image_url = image_urlNode[0].text
        # print("\n\nimage_url = ", image_url)

        small_image_urlNode = root.findall("./book/small_image_url")
        small_image_url = small_image_urlNode[0].text
        # print("\n\nsmall_image_url = ", small_image_url)
        
        allAuthors = ""
        authorsNodes = root.findall("./book/authors/author/name")
        i = 0
        for nodes in authorsNodes:
            if allAuthors != "":
                allAuthors = allAuthors + "|"
            authorName = authorsNodes[i].text
            allAuthors = allAuthors + authorName
            i += 1
        #print("\n\nallAuthors = ", allAuthors)
        print("\n\n")


        return {
            "grBookID": grBookID,
            "isbn": isbn,
            "asin": asin,
            "kindle_asin": kindle_asin,
            "bookID": bookID,
            "title": title,
            "description": description,
            "image_url": image_url,
            "small_image_url": small_image_urlNode,
            "author": allAuthors
        }


    except (KeyError, TypeError, ValueError):
        print("An error occurred trying to parse content of response\n\n")
        return None
        
    return None


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
        print(f"The response is {response.content}")
        grBookID = str(response.content, 'utf-8')
        print(f"Calling grLookupByID with grBookID = {grBookID}")
        book = grLookupByID(grBookID)
        print(f"grLookupByISBN:  book = {book}")
        return None
    except (KeyError, TypeError, ValueError):
        print(f"There was an exception raised in function grLookupByISBN({grISBN}) trying to read the response \n\n")
        return None


def goodreadsLookup():
    # https://flask-bookreviews.herokuapp.com/launchTask/goodreadsLookup
    filter = "%grish%")
    books = Book.query.filter(Book.author.like(filter)).all()
    for book in books:
        grISBN = book.isbn
        grLookupByISBN(grISBN)


def foo(start=0, end=10):
    i=0
    for x in range(start, end):
        i += 1
        print("In test worker:  x = ", x)
    return(i)
