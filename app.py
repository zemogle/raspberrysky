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
    return json.dumps({'pid':task.id})

@app.route('/status', methods=['GET'])
def check_camera_exposure():
    if 'pid' in request.args:
        pid = request.args['pid']
        return check_image_status(taskid=pid)
    else:
        return json.dumps({'status':'FAILED'})

# This is the celery task that will be run by the worker in the background
# We need to give it the celery decorator to denote this


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=8000)
