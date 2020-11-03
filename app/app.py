from flask import Flask
from celery import Celery
import os

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = os.getenv("CELERY_BROKER_URL")
app.config['RESULT_BACKEND'] = os.getenv("CELERY_RESULT_BACKEND")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

celery = Celery(app.import_name,
                backend=app.config['RESULT_BACKEND'],
                broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
