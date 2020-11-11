import time
import numpy as np
import logging
import subprocess
import signal
import sys
import time
import os
import json

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT,level=logging.DEBUG)
logger = logging.getLogger('imgserver')

def camera_active():
    # is the camera running?
    cmd = "ps aux |grep raspistill -n -w"
    lines = subprocess.check_output(cmd,shell=True)
    for line in lines.decode("utf-8").split('\n'):
        if '-awb off' in line:
            return True
    return False


def single_image_raspistill(filename='test.jpg', exp=20000000):
    if camera_active():
        return False
    annot = "%Y-%m-%d  %H:%M:%S"
    cmd = f"raspistill -n -w 1012 -h 760 -ISO 800 -ss {exp} -awb off -a 8 -a '{annot}' -o {filename}"
    proc = subprocess.Popen(cmd.split(), shell=False)
    for n in range(0,100):
        if proc.poll() is None:
            time.sleep(0.5)
            proc.send_signal(signal.SIGUSR1)
    if proc.returncode == 0:
        sys.stdout.write(f'Image {filename} Captured')
    else:
        sys.stderr.write(f'Problem with camera')
        sys.stderr.write(f"{proc.stderr}")
    return proc.pid

def check_image_status(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return json.dumps({'status':'complete'})
    else:
        return json.dumps({'status':'runnning'})

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
