import picamera
from datetime import datetime
import time
from fractions import Fraction
from PIL import Image, ImageChops
import numpy as np
import logging
from io import BytesIO
from fractions import Fraction

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT,level=logging.DEBUG)
logger = logging.getLogger('imgserver')

def image_burst(max_length):
    images = []
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        # camera.start_preview()
        camera.framerate = Fraction(1, 6)
        camera.shutter_speed = 6000000 #6s
        camera.iso = 800
        camera.awb_mode = 'off'
        camera.color_effects = (128,128)
        logger.debug('Starting image capture')
        time.sleep(1)
        for i, filename in enumerate(camera.capture_continuous('image{counter:02d}.jpg')):
            logger.debug('Captured image %s' % filename)
            images.append(filename)
            if i == max_length:
                break
        # camera.stop_preview()
    camera.close()
    return images

def single_image_capture():
    stream = BytesIO()
    with picamera.PiCamera(framerate=Fraction(1, 200),sensor_mode=3,resolution = (1280, 720)) as camera:
        #camera.start_preview()
        camera.shutter_speed = 30000000
        camera.iso = 800
        camera.awb_mode = 'off'
        # Give the camera some time to adjust to conditions
        time.sleep(2)
        camera.capture(stream, 'jpeg')
    stream.seek(0)
    yield stream.read()

    # reset stream for next frame
    stream.seek(0)
    stream.truncate()

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

def make_image(data, filename):
    '''
    Function to read in the image array
    - Write image array to a file
    '''
    #data1 = data.reshape(data.shape[0]*data.shape[1])
    logger.debug('Starting image scaling')
    img_data = scale_data(data)
    result = Image.fromarray(img_data.astype(np.uint8))
    result.save(filename)
    logger.debug('Saved image stack to file %s' % filename)
    return filename

def image_stack(images):
    filename = "combined-%s.png" % datetime.now().strftime("%Y-%m-%dT%H%M%S")
    im=np.array(Image.open(images[0]),dtype=np.float32)
    for img in images[1:]:
        currentimage=Image.open(img)
        im += np.array(currentimage, dtype=np.float32)
    make_image(im, filename)
    return filename




if __name__ == '__main__':
    max_length=2
    file_list = single_image_capture()
    combined_file = image_stack(file_list)
