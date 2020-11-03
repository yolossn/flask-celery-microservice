from app.app import celery
import time
import random


@celery.task(name="report", acks_late=True)
def report():
    print("Generating report")
    time_span = random.randint(2,120)
    time.sleep(time_span)
    return {"state":"completed"}
