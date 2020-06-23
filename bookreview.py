from app import create_app, db
from app.models import People, Book, BookReview

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'People': People, 'Book': Book, 'BookReview': BookReview}

