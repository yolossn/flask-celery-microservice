from app.app import celery
import time
import random


@celery.task(name="report", acks_late=True)
def report():
    print("Generating report")
    time.sleep(60)
    return {"state":"completed"}
