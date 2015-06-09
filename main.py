from flask import Flask
from flask import render_template
import glob
import os
import time
import allsky

app = Flask(__name__)

MAX_FILES = 150
IMAGE_DIR = '/home/pi/images/'
BASE_URL = '/images/'
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
SNAPSHOT_DIR = os.path.join(CURRENT_PATH,IMAGE_DIR)

@app.route('/')
def hello(name=None):
    files = [(BASE_URL+os.path.basename(x), time.ctime(os.path.getctime(x))) for x in glob.glob(SNAPSHOT_DIR + '*.jpg')]
    lastimage =  files[-1]
    return render_template('hello.html', filelist=files,lastimage=lastimage)

@app.route('/snap/',methods=['GET', 'POST'])
def snap(name=None):
    if request.method == 'GET':
        files = [x  for x in glob.glob(IMAGE_DIR + '*.jpg')]
        filename =  files[-1]
    if request.method == 'POST':
        filename = allsky.snap()
    return render_template('say_cheese.html', lastimage=filename, url=BASE_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0')