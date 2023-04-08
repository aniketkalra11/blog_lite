from app import worker
from datetime import datetime

celery = worker.celery

@celery.task()
def just_say_hello(name:str):
    print('inside celery task')
