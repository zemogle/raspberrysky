from datetime import datetime
import time
from fractions import Fraction
from PIL import Image, ImageChops
import numpy as np
import logging
from io import BytesIO
import subprocess
import signal
import sys
import time

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT,level=logging.DEBUG)
logger = logging.getLogger('imgserver')


def single_image_raspistill(filename='test.jpg', exp=200000000):
    now = datetime.utcnow()
    annot = "Cardiff %Y-%m-%d %X"
    cmd = f"raspistill -n -w 1012 -h 760 -ISO 800 -ss {exp} -awb off -a 8 {annot} -o {filename}"
    proc = subprocess.Popen(cmd.split(), shell=False)
    if proc.poll() is None:
        time.sleep(0.5)
        proc.send_signal(signal.SIGUSR1)
    if proc.returncode == 0:
        sys.stdout.write(f'Image {filename} Captured')
    else:
        sys.stderr.write(f'Problem with camera')
        sys.stderr.write(proc.stderr)
    return

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
    single_image_raspistill()
