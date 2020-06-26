web: flask db upgrade; flask translate compile; gunicorn bookreview:app
worker: rq worker -u $REDIS_URL flask-bookreviews-tasks
clock: python clock.py