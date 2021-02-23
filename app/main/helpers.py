import os
import requests
import urllib.parse
import xml.etree.ElementTree as ET
from app import db
from app.models import Book
import math
import locale


def grLookupByISBN(grISBN):
    """Look up quote for symbol."""
    # https://docs.python.org/3.4/library/xml.etree.elementtree.html
    
    return None

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
        
        try:
           bookIDNode = root.findall("./book/id")
           gr_bookid = bookIDNode[0].text
        except:
           gr_bookid = ""
        #print("gr_bookid = ", gr_bookid)
        
        try:
           isbnNode = root.findall("./book/isbn")
           isbn = isbnNode[0].text
           if isbn:
               isbn.strip()
        except:
            isbn = ""
        #print("isbn = ", isbn)

        try:
           isbn13Node = root.findall("./book/isbn13")
           isbn13 = isbnNode13[0].text
           if isbn13:
               isbn13.strip()
        except:
            isbn13 = ""
        #print("isbn13 = ", isbn)

        try:
            asinNode = root.findall("./book/asin")
            asin = asinNode[0].text
            if asin:
                asin.strip()
        except:
            asin = ""
        #print("asin = ", asin)

        try:
            kindle_asinNode = root.findall("./book/kindle_asin")
            kindle_asin = kindle_asinNode[0].text
            if kindle_asin:
                kindle_asin.strip()
        except:
            kindle_asin = ""
        #print("kindle_asin = ", kindle_asin)
        
        amazon_lookup_id = asin
        if amazon_lookup_id is None or amazon_lookup_id == "":
            amazon_lookup_id = kindle_asin
        if amazon_lookup_id is None or amazon_lookup_id == "":
            amazon_lookup_id = isbn
        #print("amazon_lookup_id = ", amazon_lookup_id)

        try:
            titleNode = root.findall("./book/title")
            title = titleNode[0].text
        except:
            title = ""
        #print("title = ", title)
        
        try:
            descriptionNode = root.findall("./book/description")
            description = "<h6><small>" + descriptionNode[0].text + "</small></h6>"
        except:
            description = ""
        #print("\n\ndescription = ", description)

        try:
            image_urlNode = root.findall("./book/image_url")
            image_url = image_urlNode[0].text
        except:
            image_url = ""
        #print("\n\nimage_url = ", image_url)

        try:
            small_image_urlNode = root.findall("./book/small_image_url")
            small_image_url = small_image_urlNode[0].text
        except:
            small_image_url = ""
        #print("\n\nthumbnail_url = ", small_image_url)

        try:
            average_ratingNode = root.findall("./book/average_rating")
            average_rating = average_ratingNode[0].text
        except:
            average_rating = 0
        #print("average_rating = ", average_rating)

        bookStars = {}
        try:
            rating_distNode = root.findall("./book/work/rating_dist")
            rating_dist = rating_distNode[0].text
            starsDistribution = rating_dist.split("|")
            for starsList in starsDistribution:
                stars = starsList.split(":")
                bookStars[stars[0]] = stars[1]
        except:
            rating_dist = ""
        #print("rating_dist = ", rating_dist)

        stars_1 = bookStars.get('1', 0)
        stars_2 = bookStars.get('2', 0)
        stars_3 = bookStars.get('3', 0)
        stars_4 = bookStars.get('4', 0)
        stars_5 = bookStars.get('5', 0)
        
        #print(f"5 stars = {stars_5}")
        #print(f"4 stars = {stars_4}")
        #print(f"3 stars = {stars_3}")
        #print(f"2 stars = {stars_2}")
        #print(f"1 stars = {stars_1}")
        #print("\n")
        
        allAuthors = ""
        try:
            authorsNodes = root.findall("./book/authors/author/name")
            i = 0
            for nodes in authorsNodes:
                if allAuthors != "":
                    allAuthors = allAuthors + "|"
                authorName = authorsNodes[i].text
                allAuthors = allAuthors + authorName
                i += 1
        except:
            allAuthors = ""
        #print("\n\nallAuthors = ", allAuthors)
        
        try:
            ratings_countNode = root.findall("./book/work/ratings_count")
            ratings_count = ratings_countNode[0].text
        except:
            ratings_count = 0
        #print("ratings_count = ", ratings_count)
        
        try:
            text_reviews_countNode = root.findall("./book/work/text_reviews_count")
            review_count = text_reviews_countNode[0].text
        except:
            review_count = 0
        #print("reviews_count = ", review_count)

        

        #print("\n\n")


        return {
            "gr_bookid": gr_bookid,
            "amazon_lookup_id": amazon_lookup_id,
            "isbn": isbn,
            "isbn13": isbn13,
            "asin": asin,
            "kindle_asin": kindle_asin,
            "amazon_lookup_id": amazon_lookup_id,
            "title": title,
            "description": description,
            "image_url": image_url,
            "thumbnail_url": small_image_url,
            "author": allAuthors,
            "ratings_count": ratings_count,
            "review_count": review_count,
            "average_score": average_rating,
            "stars_1": stars_1,
            "stars_2": stars_2,
            "stars_3": stars_3,
            "stars_4": stars_4,
            "stars_5": stars_5
        }


    except (KeyError, TypeError, ValueError):
        print("An error occurred trying to parse content of response\n\n")
        return None
        
    return None


def googleLookupByISBN(isbn):
    """Look up quote for symbol."""
    # https://docs.python.org/3.4/library/xml.etree.elementtree.html

    # Contact API
    try:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")        
        response.raise_for_status()
    except requests.RequestException:        
        return None

    try:
        book = response.json()
        image_url = book["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
        return image_url


    except (KeyError, TypeError, ValueError):
        print("An error occurred trying to parse content of response\n\n")
        return None
        
    return None
    

def googleLookup(source):
    """Look up quote for symbol."""
    # https://docs.python.org/3.4/library/xml.etree.elementtree.html

    # Contact API
    try:
        print(f"\n\nCalling googleapis with url https://www.googleapis.com/books/v1/volumes?q={source}")
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={source}")
        response.raise_for_status()
    except requests.RequestException:        
        return None

    try:
        count = 0
        bookIDs = []
        isbns=[]
        book = response.json()
        
        print("\n\n")
        for item in book["items"]:
        
            isbn = ""
            title = ""
            authors=""
            year = 0
            review_count = 0
            ratings_count = 0
            average_score = 0.0
            gr_bookid = 0
            asin = ""
            kindle_asin = ""
            isbn13 = ""
            stars_1 = 0
            stars_2 = 0
            stars_3 = 0
            stars_4 = 0
            stars_5 = 0
            image_url = ""
            thumbnail_url = ""
            description = ""
            amazon_lookup_id = ""
            google_image_url = ""
            homepage_image_url = ""


           
            industryIDs = item["volumeInfo"]["industryIdentifiers"]
            for id in industryIDs:
                try:
                    type = id["type"] 
                    value = id["identifier"]
                    if type == "ISBN_10":
                        isbn = value
                    if type == "ISBN_13":
                        isbn13 = value
                except:
                    isbn = ""
                    isbn13 = ""
           
            try:
                title = item["volumeInfo"]["title"]
            except:
                title = ""
                
            try:
                for oneAuthor in item["volumeInfo"]["authors"]:
                    if authors != "":
                        authors += ", "
                    authors += oneAuthor
            except:
                authors=""


            try:
                year = (item["volumeInfo"]["publishedDate"])[0:4]
            except:
                year = 0

           
            try:
                image_url = item["volumeInfo"]["imageLinks"]["thumbnail"]
                thumbnail_url = image_url
                google_image_url = image_url
                homepage_image_url = image_url
            except:
                image_url = ""
                thumbnail_url = ""
                google_image_url = ""
                homepage_image_url = ""


            try:
                description = item["volumeInfo"]["description"]
            except:
                description = ""
                
  
            print(f"\n\nisbn = {isbn}")
            print(f"title = {title}")
            print(f"isbn13 = {isbn13}")
            print(f"authors = {authors}")
            print(f"year = {year}")
            print(f"image_url = {image_url}")
            
            # If we have the ISBN in our DB, just update the pictures and the description.
            
            ourBook = Book.query.filter(Book.isbn == isbn).first()
            
            if ourBook != None:
                # Update the images and description
                print(f"Found isbn {ourBook.isbn}, id = {ourBook.id}")
                ourBook.set_amazon_lookup_id(isbn)
                ourBook.set_image_url(image_url)
                ourBook.set_isbn13(isbn13)
                ourBook.set_thumbnail_url(image_url)
                ourBook.set_google_image_url(image_url)
                ourBook.set_homepage_image_url(image_url)
                ourBook.set_description = description
                
                db.session.commit()
                count += 1
                bookIDs.append(ourBook.id)
                isbns.append(isbn)
                
            else:
                print(f"\n\nThis is a new book that is being added to our DB")
                newBook = Book(isbn=isbn,
                               title=title,
                               author=authors,
                               year=year,
                               amazon_lookup_id=isbn,
                               image_url=image_url,
                               thumbnail_url=image_url,
                               google_image_url=image_url,
                               homepage_image_url=image_url,
                               description=description,
                               review_count = 0,
                               ratings_count = 0,
                               average_score = 0,
                               asin = isbn,
                               kindle_asin = isbn,
                               stars_1 = 0,
                               stars_2 = 0,
                               stars_3 = 0,
                               stars_4 = 0,
                               stars_5 = 0
                               )
                db.session.add(newBook)
                db.session.commit()
                count += 1
                bookIDs.append(newBook.id)
                isbns.append(isbn)
                print(f"Added new book id = {newBook.id}")




#            # Look up the book in goodreads
#            # First get the goodreads book ID by isbn
#            print(f"\n\nLook up goodreads isbn {isbn}")
#            goodreadsBookID = grLookupByISBN(isbn)
#            if goodreadsBookID != None:
#                print(f"Found goodreadsBookID {goodreadsBookID} for isbn {isbn}")
#                # Get the ratings from gooreads
#                goodreadsBook = grLookupByID(goodreadsBookID)
#                if ourBook != None:
#                    print(f"\n\nWe have this book in our DB, id = {ourBook.id}, bookreads id = {goodreadsBookID}")
#                    ourBook.set_review_count(goodreadsBook["review_count"])
#                    ourBook.set_ratings_count(goodreadsBook["ratings_count"])
#                    ourBook.set_average_score(goodreadsBook["average_score"])
#                    ourBook.set_asin(goodreadsBook["asin"])
#                    ourBook.set_kindle_asin(goodreadsBook["kindle_asin"])
#                    ourBook.set_stars_1(goodreadsBook["stars_1"])
#                    ourBook.set_stars_2(goodreadsBook["stars_2"])
#                    ourBook.set_stars_3(goodreadsBook["stars_3"])
#                    ourBook.set_stars_4(goodreadsBook["stars_4"])
#                    ourBook.set_stars_5(goodreadsBook["stars_5"])
                    
                    
#                    db.session.commit()
#                    count += 1
#                    bookIDs.append(ourBook.id)
#                    isbns.append(isbn)


#                else:
#                    # Add the book to our DB
#                    print(f"\n\nThis is a new book that is being added to our DB, bookreads id = {goodreadsBookID}")
#                    newBook = Book(isbn=isbn,
#                                   title=title,
#                                   author=authors,
#                                   year=year,
#                                   amazon_lookup_id=isbn,
#                                   gr_bookid=goodreadsBookID,
#                                   isbn13=isbn13,
#                                   image_url=image_url,
#                                   thumbnail_url=image_url,
#                                   google_image_url=image_url,
#                                   homepage_image_url=image_url,
#                                   description=description,
#                                   review_count = goodreadsBook["review_count"],
#                                   ratings_count = goodreadsBook["ratings_count"],
#                                   average_score = goodreadsBook["average_score"],
#                                   asin = goodreadsBook["asin"],
#                                   kindle_asin = goodreadsBook["kindle_asin"],
#                                   stars_1 = goodreadsBook["stars_1"],
#                                   stars_2 = goodreadsBook["stars_2"],
#                                   stars_3 = goodreadsBook["stars_3"],
#                                   stars_4 = goodreadsBook["stars_4"],
#                                   stars_5 = goodreadsBook["stars_5"]
#                                   )
#                    db.session.add(newBook)
#                    db.session.commit()
#                    count += 1
#                    bookIDs.append(newBook.id)
#                    isbns.append(isbn)
#                    print(f"Added new book id = {newBook.id}")
                    
#            else:
#                print(f"COULD NOT FIND goodreadsBookID for isbn {isbn}")

        
        return {
           "count": count,
           "isbns": isbns,
           "bookIDs":bookIDs
        }



    except (KeyError, TypeError, ValueError):
        print("An error occurred trying to parse content of response\n\n")
        return None
        
    return None





def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def pct(value):
    """Format value as percent."""
    return f"{value:,.2f}"
    
def formatByLocale(value):
    locale.setlocale(locale.LC_ALL, '')
    return f'{value:n}'


def stringSlice(source,charater,position):
    """ Return some part of a string."""
    """ Example: stringSlice(".", 0, 1) """
    value = source.split(charater)[position]
    return f"{value}"
