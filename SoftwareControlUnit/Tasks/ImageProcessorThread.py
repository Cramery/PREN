import threading
import cv2
import numpy as np

class ImageProcessorThread(threading.Thread):
    def __init__(self, owner):
        super(ImageProcessorThread, self).__init__()
        self.isTerminated = False
        self.isStopSignFound = True
        self.owner = owner
        self.startSignDetectionEvent = threading.Event()
        self.start()
        print("IPCT: Image Processing Thread started")
        # set up for the color range
        self.color_lower_range = [106, 100, 55]
        self.color_upper_range = [114, 255, 255]
        # set the size of alloud start/stop area
        self.min_area_of_startstop = 1000
        self.max_area_of_startstop = 10000

    def run(self):
        self.startSignDetectionEvent.clear()
        while not self.isTerminated:
            while not self.isStopSignFound:
                for img in self.imagestream:
                    self.__checkStartSignal(img)
                    if self.isStopSignFound:
                        print("IPCT: STOP SIGN REALLY FOUND!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        self.owner.StartSignCounter += 1
                        break
                self.startSignDetectionEvent.clear()

    def SetImageStreamAndStart(self, imagestream):
        print("IPCT: Setup IPCT with stream")
        self.imagestream = imagestream
        self.isStopSignFound = False
        self.startSignDetectionEvent.set()

    def FinishThread(self):
        print("IPCT: Image Processing Thread stopped")
        self.isTerminated = True

    def __checkStartSignal(self, img):
        # converting frame(img) from BGR (Blue-Green-Red) to HSV (hue-saturation-value)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # defining the range of Blue color
        blue_lower = np.array(self.color_lower_range, np.uint8)
        blue_upper = np.array(self.color_upper_range, np.uint8)

        # finding the range blue colour in the image
        blue = cv2.inRange(hsv, blue_lower, blue_upper)

        # Morphological transformation, Dilation
        kernal = np.ones((5, 5), "uint8")

        blue = cv2.dilate(blue, kernal)
        res = cv2.bitwise_and(img, img, mask=blue)

        # Tracking Colour (blue)
        contours, hierarchy = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # save the data of the detected
        detectedRectangle = []

        # looking for rectangles
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > self.min_area_of_startstop and area < self.max_area_of_startstop):
                x, y, w, h = cv2.boundingRect(contour)
                schnitt = w / h
                if (schnitt < 4 and schnitt > 2):
                    # draw  a rectangle of every detected blue object
                    # img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    # print(area)

                    # save the data of the rectangle
                    # x start coordinate, x end coordinate, y start coordinate, width, heigth
                    detectedRectangle.append([x + 1, x + w, y, w, h])

        # needed for iteration of the rectangle array
        current = 0
        next = 1
        detectedRectangle.sort()

        # detected object need to start and end at the same/near x-coordinate.
        # if the rectangle match, draw a red rectangle around
        while (next < len(detectedRectangle)):
            differenceDetectedPanelPosition = detectedRectangle[current][0] / detectedRectangle[next][0]
            diffeenceDetectedPanelWidth = detectedRectangle[current][1] / detectedRectangle[next][1]
            if (differenceDetectedPanelPosition > 0.8 and differenceDetectedPanelPosition < 1.2 and diffeenceDetectedPanelWidth > 0.8 and diffeenceDetectedPanelWidth < 1.2):
                print("IPCT: Stopsign found")
                self.isStopSignFound = True

                img = cv2.rectangle(img, (detectedRectangle[current][0], detectedRectangle[current][2]), (
                    detectedRectangle[current][1], detectedRectangle[current][2] + detectedRectangle[current][4]),
                                    (0, 0, 255), 3)
                img = cv2.rectangle(img, (detectedRectangle[next][0], detectedRectangle[next][2]), (
                    detectedRectangle[next][1], detectedRectangle[next][2] + detectedRectangle[next][4]),
                                    (0, 0, 255), 3)
                self.isStopSignFound
                print("IPCT: Startsign detected")
                return
            current += 1
            next += 1