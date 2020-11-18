from celery import Celery

from allsky import single_image_raspistill

celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery.task
def background_task():
    # some long running task here (this simple example has no output)
    pid = single_image_raspistill(filename='static/snap.jpg', exp=120000000)
