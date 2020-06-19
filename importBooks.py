import psycopg2
import os

#  DATABASE_URL=postgresql://postgres:oatmeal@localhost:5432/BookReview

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