#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, send_from_directory, request
import socket
import json

from allsky import single_image_raspistill, check_image_status
from tasks import background_task

app = Flask(__name__)

# Create the Celery instance, referring to the task queue (or broker) as redis

@app.route('/')
def index():
    """All sky streaming home page."""
    return render_template('index.html', name=socket.gethostname())

#background process happening without any refreshing
@app.route('/snap')
def background_process():
    task = background_task.apply_async()
    return json.dumps({'pid':pid})

@app.route('/status', methods=['GET'])
def check_camera_exposure():
    if 'pid' in request.args:
        pid = int(request.args['pid'])
        return check_image_status(pid=pid)
    else:
        return json.dumps({'status':'failed'})

# This is the celery task that will be run by the worker in the background
# We need to give it the celery decorator to denote this


# Create a flask route - this is a simpl get request
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        # add the background task to the task queue,
        # arguments for the task: arg1=10, arg2=20
        # optionally countdown specifies a 60 second delay
        task = my_background_task.apply_async(args=[10, 20], countdown=60)

    # Flask returns this message to the browser
    return {'task started'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=8000)
