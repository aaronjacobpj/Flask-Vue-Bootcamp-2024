"""Entry point for Celery.

Run each in its own terminal (from the backend folder):
    celery -A worker.celery worker --loglevel=info      # executes jobs
    celery -A worker.celery beat   --loglevel=info      # triggers scheduled jobs
"""
from app import app
import application.tasks  # noqa: F401  (registers the tasks)

celery = app.extensions["celery"]
