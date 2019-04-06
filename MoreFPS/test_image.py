import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1920, 1080)
    camera.start_preview()
    # Camera warm-up time
    time.sleep(0.1)
    camera.capture('testFoto.jpg', resize=(320, 240))
