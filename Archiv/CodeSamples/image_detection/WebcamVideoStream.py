from threading import Thread
import cv2
from time import sleep

class WebcamVideoStream:
    def __init__(self, src):
        #initialize the video camera and read the first image
        #from the stream
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()

        #Initialize variable to Check if thread is stopped
        self.stopped = False

    def start(self):
        # Start the Thread, give the update method to work on and then when the Thread is created
        # just execute .start() on it
        # 'target = self.update Just call update method as instruction instead of run()
        # 'args = take empty argments as ....?
        Thread(target=self.update, args=()).start()
        return

    def update(self):
        #Keep on looping until the thread stopped = True
        while True:
            if self.stopped:
                return

            #read next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True