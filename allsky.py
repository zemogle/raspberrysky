import picamera
from datetime import datetime
import time
from fractions import Fraction
from PIL import Image, ImageChops
import numpy as np
import logging
from io import BytesIO

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT,level=logging.DEBUG)
logger = logging.getLogger('imgserver')

def single_image_stream():
    stream = BytesIO()
    with picamera.PiCamera(framerate=Fraction(1, 10),sensor_mode=3,resolution = (1280, 720)) as camera:
        #camera.start_preview()
        camera.shutter_speed = 10000000
        camera.iso = 800
        camera.awb_mode = 'off'
        camera.exposure_mode = 'off'
        # Give the camera some time to adjust to conditions
        time.sleep(20)
        camera.capture(stream, 'jpeg')
    stream.seek(0)
    yield stream.read()

    # reset stream for next frame
    stream.seek(0)
    stream.truncate()

def single_image_capture(filename):
    camera = picamera.PiCamera()
    #camera.start_preview()
    camera.iso = 800
    # Give the camera some time to adjust to conditions
    camera.resolution = (1024, 768)
    camera.start_preview()
    time.sleep(20)
    camera.capture(filename)
    return filename

def scale_data(data):
    '''
    Scale image
    - Find the 99.5% value
    - Make all values above 99.5% value white
    '''
    data[data<0.]=0.
    median = np.median(data)
    data-= median
    data[data<0.]=0.
    sc_data= data #np.arcsinh(data)
    max_val = np.percentile(sc_data,99.5)
    logging.warning('99.5 =%s' % max_val)
    scaled = sc_data*255./(max_val)
    scaled[scaled>255]=255
    logging.warning('Median of scaled=%s' % np.median(scaled))
    logging.warning('Min scaled=%s' % scaled.min())
    return scaled


if __name__ == '__main__':
    file_list = single_image_capture('test.jpg')
