import time
from rq import get_current_job
from app.main.helpers import grLookupByID, grLookupByISBN, goodreadsLookup

from app import create_app

app = create_app()
app.app_context().push()

def example(intervalInSecods):
    try:
        seconds = int(intervalInSecods)
    except ValueError:
        seconds = 60

    job = get_current_job()
    print('Starting Task')
    for i in range(seconds):
        job.meta['progress'] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task completed')


def queryGoodReads(grISBN=""):
    job = get_current_job()
    if grISBN:
        print(f"Starting Task queryGoodReads for a list of ISBN")
        goodreadsLookup()
    else:
        print(f"Starting Task queryGoodReads with ISBN {grISBN}")
        grLookupByISBN(grISBN)