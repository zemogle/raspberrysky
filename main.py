from flask import Flask
from flask import render_template
import glob
import os
import time

app = Flask(__name__)

MAX_FILES = 150
IMAGE_DIR = 'static/picam/'
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
SNAPSHOT_DIR = os.path.join(CURRENT_PATH,IMAGE_DIR)

@app.route('/')
def hello(name=None):
    files = [('picam/'+os.path.basename(x), time.ctime(os.path.getctime(x))) for x in glob.glob(SNAPSHOT_DIR + '*.jpg')]
    print files
    lastimage =  files[-1]
    return render_template('hello.html', filelist=files,lastimage=lastimage)

if __name__ == '__main__':
    app.run()