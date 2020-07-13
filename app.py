#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, send_from_directory
import socket

from allsky import single_image_raspistill, single_image_stream

app = Flask(__name__)

@app.route('/')
def index():
    """All sky streaming home page."""
    return render_template('index.html', name=socket.gethostname())

@app.route('/snap.jpg')
def latest_image():
    ''' Static image snapshot, useful for timelapse '''
    return Response(single_image_stream(), mimetype='image/jpeg')

#background process happening without any refreshing
@app.route('/snap')
def background_process_test():
    single_image_raspistill(filename='static/snap.jpg')
    return ("nothing")

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=8000)
