#/usr/bin/python
import urllib2, urllib
import time, os
from datetime import datetime
import RPi.GPIO as GPIO
import picamera


data = {
    "token": "aXE6iizBUepbGFTwAf7bgKF5VA2bas",
    "user": "uwzheVMRmga3QAFzb72cX1DwnZxupZ",
    "message": "Ding Dong!",
    "device" : "iPhone"
    "url_title" : "Who is at the door"
  }
  
SNAPSHOT_DIR = os.path.join(CURRENT_PATH,'/static/images')
  
def __main__():
    url = 'https://api.pushover.net/1/messages.json'
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    while True:
        GPIO.wait_for_edge(23, GPIO.FALLING)
        print "Button pressed"
        filename = snap()
        ip = myip()
        img_url = "http://%s:8080/static/images/%s" % (ip,filename)
        data['url'] = img_url
        dataenc = urllib.urlencode(data)
        content = urllib2.urlopen(url=url, data=dataenc).read()
        GPIO.wait_for_edge(23, GPIO.RISING)
        print("Button Released")
    GPIO.cleanup()
    
def snap():
    filename = "image-%s.jpg" % datetime.strftime(datetime.now(),"%Y-%m-%dT%H:%M:%S")
    camera = picamera.PiCamera()
    camera.led = False
    camera.resolution = (800,600)
    #camera.shutter_speed = 20000
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    camera.capture(SNAPSHOT_DIR +filename)
    return filename
    
def myip():
    url = 'http://ipecho.net/plain'
    f = urllib2.urlopen(url)
    ip = f.read()
    return ip
    
__main__()
