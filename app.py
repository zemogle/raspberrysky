#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, send_from_directory
import socket

from allsky import single_image_raspistill, check_image_status

app = Flask(__name__)

@app.route('/')
def index():
    """All sky streaming home page."""
    return render_template('index.html', name=socket.gethostname())

#background process happening without any refreshing
@app.route('/snap')
def background_process_test():
    single_image_raspistill(filename='static/snap.jpg')
    return ("nothing")

@app.route('/status', methods=['GET'])
def check_camera_exposure():
    if 'pid' in request.args:
        pid = int(request.args['pid'])
        return check_image_status(pid=pid)
    else:
        return json.dumps({'status':'failed'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=8000)
