import time
from rq import get_current_job
from app.main.helpers import grLookupByID
from app.tasks.helpers import grLookupByISBN, grLookupIDByISBN

from app import create_app

app = create_app()
app.app_context().push()

def task_example(intervalInSecods):
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


def task_grLookupByISBN(grISBN):
    job = get_current_job()
    print(f"Starting task_grLookupByISBN with ISBN {grISBN}")
    grLookupByISBN(grISBN)


def task_grLookupIDByISBN():
    job = get_current_job()
    print(f"Starting task_grLookupIDByISBN with no arguments")
    grLookupIDByISBN()