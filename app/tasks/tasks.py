import time
from rq import get_current_job
from app.main.helpers import grLookupByID
from app.tasks.helpers import grLookupByISBN, grUpdateIDByISBN, booksUpdateByGRID

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
    print('task_example completed')


def task_example(seconds):
    https://flask-bookreviews.herokuapp.com/tasks/launchTask/task_example/60
    job = get_current_job()
    print(f"Starting task_example with number of seconds {seconds}")
    example(60)



def task_grLookupByISBN(grISBN):
    job = get_current_job()
    print(f"Starting task_grLookupByISBN with ISBN {grISBN}")
    grLookupByISBN(grISBN)


def task_grUpdateIDByISBN():
    # https://flask-bookreviews.herokuapp.com/tasks/launchTask/task_grUpdateIDByISBN
    
    job = get_current_job()
    print(f"Starting task_grUpdateIDByISBN with no arguments")
    grUpdateIDByISBN()

def task_updateBooksByGRID():
    # https://flask-bookreviews.herokuapp.com/tasks/launchTask/task_updateBooksByGRID
    
    job = get_current_job()
    print(f"Starting task_updateBooksByGRID with no arguments")
    booksUpdateByGRID()
