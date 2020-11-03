from app.app import celery
import time
import random


@celery.task(name="report")
def report():
    print("Generating report")
    time_span = random.randint(2,7)
    time.sleep(time_span)
    return {"state":"completed"}
