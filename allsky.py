import picamera
from datetime import datetime
import time
from fractions import Fraction
from PIL import Image, ImageChops
import numpy
import logging

FORMAT = '%(asctime)-15s  %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT,level=logging.DEBUG)
logger = logging.getLogger('imgserver')

def snap(max_length):
    images = []
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        # Set a framerate of 1/6fps, then set shutter
        camera.framerate = Fraction(1, 6)
        #camera.shutter_speed = 6000000 #6s
        camera.iso = 800
        camera.awb_mode = 'off'
        camera.color_effects = (128,128)
        # This gives ISO of 1250
        # camera.exposure_mode = 'sports'
        logger.debug('Starting image capture')
        for filename in camera.capture_continuous('img{timestamp:%Y-%m-%d-%H%M%S}.png'):
            logger.debug('Captured %s' % filename)
            images.append(filename)
            if len(images) == max_length:
                break
        camera.stop_preview()
    camera.close()
    return images

def image_array_capture():
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        #camera.start_preview()
        camera.shutter_speed = 6000000
        camera.iso = 800
        camera.awb_mode = 'off'
        camera.color_effects = (128,128)
        # Give the camera some time to adjust to conditions
        time.sleep(2)
        camera.capture('foo.jpg')
    camera.close()
    # camera.stop_preview()


def make_image(data, filename):
    '''
    Function to read in the image array
    - Find the 99.5% value
    - Make all values above 99.5% value white
    - Write image array to a PNG
    '''
    #data1 = data.reshape(data.shape[0]*data.shape[1])
    logger.debug('Starting image scaling')
    max_val = numpy.percentile(data,99.5)
    scaled = data*256./max_val
    new_scaled = numpy.ma.masked_greater(scaled, 255.)
    new_scaled.fill_value=255.
    img_data = new_scaled.filled()
    result = Image.fromarray(img_data.astype(numpy.uint8))
    result.save(filename)
    logger.debug('Saved image stack to file %s' % filename)
    return filename

def image_stack(image_list):
    data=Image.open(image_list[0])
    for img in image_list[1:]:
        currentimage=Image.open(img)
        data=ImageChops.lighter(matchimage, currentimage)
        logger.debug('Adding data to the stack')
    filename = "combined-%s.png" % datetime.now().strftime("%Y-%m-%dT%H%M%S")
    make_image(data, filename)
    return filename
    # im=np.array(matchimage,dtype=np.float32)
    # for img in files[1:]:
    #     currentimage=Image.open(img)
    #     im += np.array(currentimage, dtype=np.float32)
    # im /= len(files) * 0.25 # lowered brightness, with magic factor
    # # clip, convert back to uint8:
    # final_image = Image.fromarray(np.uint8(im.clip(0,255)))
    # final_image.save('all_averaged.jpg', 'JPEG')


if __name__ == '__main__':
    max_length=2
    file_list = snap(max_length)
    combined_file = image_stack(file_list)
    print combined_file
