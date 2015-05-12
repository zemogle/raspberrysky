import web
import picamera
from time import sleep
from datetime import datetime
import glob
import os
import urllib2, urllib
import time
from datetime import datetime
from pushover1.py import snap

urls = (
    '/', 'home',
    'takesnap','snapper'
)

render = web.template.render('templates', base='base')

MAX_FILES = 150
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
SNAPSHOT_DIR = os.path.join(CURRENT_PATH,'/static/images')

class Viewer:
    def GET(self, name):
        img_url = '/static/images/' + name
        return render.home(img_url)

class snapper:
    def GET(self):
        filename = snap()
        raise web.seeother('/')

class home:
    form = web.form.Form(
        web.form.Button('Take Image'),
    )

    def getImageList(self):
        return map(os.path.basename, glob.glob(SNAPSHOT_DIR + '*.jpg'))

    def __init__(self):
        self._camLock = False

    def GET(self):
        form = self.form()
        images = self.getImageList()
        if len(images)>0:
            filename = images[0]
        else:
            filename=None
        return render.home(form, images,filename)

    def POST(self):
        form = self.form()
        if not form.validates() or self._camLock:
            return render.home(form, self.getImageList())

        filename = "image-%Y-%m-%dT%H:%m:%s.jpg" % 
        self._camLock = True
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            # Camera warm-up time
            time.sleep(2)
            camera.capture(SNAPSHOT_DIR +filename)
        self._camLock = False
        return render.home(form, self.getImageList(),filename)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()