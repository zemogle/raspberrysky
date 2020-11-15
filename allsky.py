import time
import numpy as np
import logging
import subprocess
import sys
import time
import os
import json
from redis import StrictRedis

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT,level=logging.DEBUG)
logger = logging.getLogger('imgserver')

def camera_active():
    # is the camera running?
    cmd = "ps aux |grep raspistill -n -w"
    lines = subprocess.check_output(cmd,shell=True)
    for line in lines.decode("utf-8").split('\n'):
        if '-ISO 800' in line:
            return True
    return False


def single_image_raspistill(filename='test.jpg', exp=20000000):
    if camera_active():
        return False
    annot = "%Y-%m-%dT%H:%M:%S"
    cmd = f"raspistill -n -w 1012 -h 760 -ISO 800 -ss {exp} -a 8 -a {annot} -o {filename}"

    try:
        proc = subprocess.run(cmd.split(), shell=False)
    except:
        sys.stderr.write(f'Problem with camera')
        return False
    else:
        return True

def check_image_status(taskid):
    """ Check For the existence of a unix pid. """
    connection = StrictRedis.from_url('redis://localhost:6379')
    r = connection.get(f'celery-task-meta-{taskid}')
    connection.close()
    try:
        status = json.loads(r)
    except Exception as e:
        print(e)
        return json.dumps({'status':'FAILED'})
    else:
        return json.dumps({'status':status['status']})

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
