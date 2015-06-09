import picamera
from datetime import datetime
import time
from fractions import Fraction
from PIL import Image, ImageChops

def snap():
    filename = "image-%s.png" % datetime.now().strftime("%Y-%m-%dT%H%M%S")
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        # Camera warm-up time
        time.sleep(2)
        # Set a framerate of 1/6fps, then set shutter
        camera.framerate = Fraction(1, 6)
        camera.shutter_speed = 6000000 #6s
        #camera.iso = 800
        camera.awb_mode = 'cloudy'
        # This gives ISO of 1250
        camera.exposure_mode = 'sports'
        # camera.led = False # Have to do this setting as Root
        time.sleep(10)
        camera.capture(filename)
    camera.close()
    return filename

def image_stack(image_list):
    matchimage=Image.open(image_list[0])
    filename = "combined-%s.png" % datetime.now().strftime("%Y-%m-%dT%H%M%S")
    for img in image_list[1:]:
        currentimage=Image.open(img)
        matchimage=ImageChops.lighter(matchimage, currentimage)
    matchimage.save(filename,"PNG")
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
    file_list = []
    for i in range(0,5):
        filename = snap()
        file_list.append(filename)
    combined_file = image_stack(file_list)
    print combined_file


