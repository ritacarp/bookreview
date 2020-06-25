import os
import requests
import urllib.parse
import xml.etree.ElementTree as ET
from app.models import Book
import math



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
           grBookID = bookIDNode[0].text
        except:
           grBookID = ""
        print("grBookID = ", grBookID)
        
        try:
           isbnNode = root.findall("./book/isbn")
           isbn = isbnNode[0].text
           if isbn:
               isbn.strip()
        except:
            isbn = ""
        print("isbn = ", isbn)

        try:
           isbn13Node = root.findall("./book/isbn13")
           isbn13 = isbnNode13[0].text
           if isbn13:
               isbn13.strip()
        except:
            isbn13 = ""
        print("isbn13 = ", isbn)

        try:
            asinNode = root.findall("./book/asin")
            asin = asinNode[0].text
            if asin:
                asin.strip()
        except:
            asin = ""
        print("asin = ", asin)

        try:
            kindle_asinNode = root.findall("./book/kindle_asin")
            kindle_asin = kindle_asinNode[0].text
            if kindle_asin:
                kindle_asin.strip()
        except:
            kindle_asin = ""
        print("kindle_asin = ", kindle_asin)
        
        bookID = asin
        if bookID is None or bookID == "":
            bookID = kindle_asin
        if bookID is None or bookID == "":
            bookID = isbn
        print("bookID = ", bookID)

        try:
            titleNode = root.findall("./book/title")
            title = titleNode[0].text
        except:
            title = ""
        print("title = ", title)
        
        try:
            descriptionNode = root.findall("./book/description")
            description = "<h6><small>" + descriptionNode[0].text + "</small></h6>"
        except:
            description = ""
        print("\n\ndescription = ", description)

        try:
            image_urlNode = root.findall("./book/image_url")
            image_url = image_urlNode[0].text
        except:
            image_url = ""
        # print("\n\nimage_url = ", image_url)

        try:
            small_image_urlNode = root.findall("./book/small_image_url")
            small_image_url = small_image_urlNode[0].text
        except:
            small_image_url = ""
        # print("\n\nsmall_image_url = ", small_image_url)

        try:
            average_ratingNode = root.findall("./book/average_rating")
            average_rating = average_ratingNode[0].text
        except:
            average_rating = 0
        print("average_rating = ", average_rating)

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
        print("rating_dist = ", rating_dist)

        stars_1 = bookStars.get('1', 0)
        stars_2 = bookStars.get('2', 0)
        stars_3 = bookStars.get('3', 0)
        stars_4 = bookStars.get('4', 0)
        stars_5 = bookStars.get('5', 0)
        
        print(f"5 stars = {stars_5}")
        print(f"4 stars = {stars_4}")
        print(f"3 stars = {stars_3}")
        print(f"2 stars = {stars_2}")
        print(f"1 stars = {stars_1}")
        print("\n")
        
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
        print("ratings_count = ", ratings_count)
        
        try:
            text_reviews_countNode = root.findall("./book/work/text_reviews_count")
            reviews_count = text_reviews_countNode[0].text
        except:
            reviews_count = 0
        print("reviews_count = ", reviews_count)

        

        print("\n\n")


        return {
            "grBookID": grBookID,
            "bookID": bookID,
            "isbn": isbn,
            "isbn13": isbn13,
            "asin": asin,
            "kindle_asin": kindle_asin,
            "bookID": bookID,
            "title": title,
            "description": description,
            "image_url": image_url,
            "thumbnail_url": small_image_urlNode,
            "author": allAuthors,
            "ratings_count": ratings_count,
            "reviews_count": reviews_count,
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

