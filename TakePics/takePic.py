import cv2

import io
import time
import picamera

# camera resolution
width = 640
hight = 480
# framerate
frameratio = 100
# camera warmup and duration of recording time
camera_warmup_time = 2
camera_record_time = 1 # duration of taking pics !!!


class SplitFrames(object):
    def __init__(self):
        self.frame_num = 0
        self.output = None

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; close the old one (if any) and
            # open a new output
            if self.output:
                self.output.close()
            self.frame_num += 1
            # save under, wb = open for writing/ binary mode
            self.output = io.open('Bilder/image%02d.jpg' % self.frame_num, 'wb')
        self.output.write(buf)


with picamera.PiCamera(resolution=(width, hight), framerate=frameratio) as camera:
    camera.start_preview()
    # Give the camera some warm-up time
    time.sleep(camera_warmup_time)
    # start taking the pics
    output = SplitFrames()
    start = time.time()
    camera.start_recording(output, format='mjpeg')
    # duration of recording
    camera.wait_recording(camera_record_time)
    camera.stop_recording()
    finish = time.time()
    print('Captured %d frames at %.2ffps' % (
    output.frame_num,
    output.frame_num / (finish - start)))
