import os
import requests
import urllib.parse
import xml.etree.ElementTree as ET 



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
        
        isbnNode = root.findall("./book/isbn")
        isbn = isbnNode[0].text
        # print("\n\nisbn = ", isbn)
        
        titleNode = root.findall("./book/title")
        title = titleNode[0].text
        # print("\n\ntitle = ", title)
        
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
        print("\n\nallAuthors = ", allAuthors)


        return {
            "grBookID": grBookID,
            "isbn": isbn,
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

