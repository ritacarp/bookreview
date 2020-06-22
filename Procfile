web: flask db upgrade; flask translate compile; gunicorn bookreview:app
worker: python worker.py
worker: python createRQ.py