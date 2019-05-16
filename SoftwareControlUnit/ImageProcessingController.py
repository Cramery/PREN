import time
import RPi.GPIO as GPIO
import numpy as np
from picamera import PiCamera
import os
import cv2
import io

class ImageProcessingController():
    def __init__(self, uartCommunicator, dataController):
        print("IPC: Init ImageProcessingController")
        self._uartCommunicator = uartCommunicator
        self._dataController = dataController
        #Controll
        self._stopSignDigit = 0
        self._startSignCounter = 0
        self._isStopSignFound = False
        #Cam
        self._camera = PiCamera()
        self._resolutionWidth = 640
        self._resolutionHeight = 480
        self._camera.resolution = (self._resolutionWidth, self._resolutionHeight)
        #Imagetemaplates
        self._templateArray = self._readTemplateArray("/ImageTemplates")
        #Distancemeasurement
        self._setupGPIO()
        self._distance_threshold = 60

    def LookForStartSignCaptureStream(self):
        print("IPC: started looking for START and HALTE signs")
        while self._startSignCounter <= 3:
            #todo self._dataController.SaveTopSignalStream(self.CaptureStreamInRange(True))
            self._dataController.SaveTopSignalStream(self.CaptureStream(True))
        self.SaveImageStreamToFS(self._dataController.GetTopSignalStream())
        print("IPC: 3 Rounds finished, Stopsigndigit is ".format(self._stopSignDigit))
        self._uartCommunicator.LastRoundIsFinished()

    def GetStopSignDigit(self):
        print("IPC: Get Stopsign-Digit")
        self._stopSignDigit = self._analyzeVideoStream(self._dataController.GetTopSingalStream())
        print("IPC: Stopdigit: ", self._stopSignDigit)

    def DetectStopSign(self):
        print("IPC: started looking for STOP signs")
        while not self._isStopSignFound:
            #todo self.CaptureStreamInRange(False)
            self._isStopSignFound = True
        print("IPC: Stop sign found")
        #todo Distanzmessung
        print("IPC: Stopdigit: Stop Train")
        self._uartCommunicator.StopTrain()

    ###################################################################
    # Imagedetection
    def CaptureStreamInRange(self, getTopImages = True):
        print("IPC: Look for Object in Range")
        lookForSign = True
        picameraStream = []
        #todo busy waiting vermeiden
        sleeptime = 0.1
        while lookForSign:
            # Abstandsmessung wird mittels des 10us langen Triggersignals gestartet
            GPIO.output(self._trigger_AusgangsPin, True)
            time.sleep(0.00001)
            GPIO.output(self._trigger_AusgangsPin, False)

            # Hier wird die Stopuhr gestartet
            EinschaltZeit = time.time()
            while GPIO.input(self._echo_EingangsPin) == 0:
                EinschaltZeit = time.time()  # Es wird solange die aktuelle Zeit gespeichert, bis das Signal aktiviert wird

            while GPIO.input(self._echo_EingangsPin) == 1:
                AusschaltZeit = time.time()  # Es wird die letzte Zeit aufgenommen, wo noch das Signal aktiv war

            # Die Differenz der beiden Zeiten ergibt die gesuchte Dauer
            Dauer = AusschaltZeit - EinschaltZeit
            # Mittels dieser kann nun der Abstand auf Basis der Schallgeschwindigkeit der Abstand berechnet werden
            Abstand = (Dauer * 34300) / 2

            # Überprüfung, ob der gemessene Wert unterhalb des Thresholds liegt
            if Abstand < 2 or (round(Abstand) < self._distance_threshold):
                print("IPC: Capturestream, getTopImages: ",getTopImages)
                picameraStream.append(self.CaptureStream(getTopImages))
                lookForSign = False
            else:
                time.sleep(sleeptime)
        return picameraStream

    def CaptureStream(self, getTopImages):
        streamCapture = []
        # Create the in-memory stream
        stream = io.BytesIO()
        #Set framerate, calculate recordcount
        if(getTopImages):
            self._camera.framerate = 20
            recordcount = self._camera.framerate
        else:
            self._camera.framerate = 10
            recordcount = self.camera.framerate * 2
        #Capture images and append to stream
        for count in range(0, int(recordcount)):
            self._camera.capture(stream, format='jpeg')
            # Construct a numpy array from the stream
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            # "Decode" the image from the array, preserving colour
            image = cv2.imdecode(data, 1)
            #todo opencv obj
            streamCapture.append(image)
            if (getTopImages):
                # todo Startsignalerkennung
                self._startSignCounter += 1
            else:
                pass
                # todo Stopsignalerkennung
        return stream

    def _analyzeVideoStream(self, videostream):
        print("IPC: Start Stream analysis")
        captures = self._getCroppedBoxes(videostream)
        # All the 6 methods for comparison in a list
        methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED',
                   'cv2.TM_CCOEFF', 'cv2.TM_CCORR', 'cv2.TM_SQDIFF']
        for meth in methods:
            maxwkeittemp = 0
            maxnotemp = 0
            print(str(meth))
            for capture in captures:
                # capture = cv2.resize(capture, (20, 40))
                # Get widht/height
                height, width = capture.shape
                # if capture is too small, dont do anything
                if (height > 30 & width > 18):
                    # so something
                    i = 0
                    for template in self._templateArray:
                        i += 1
                        w, h = template.shape[::-1]
                        method = eval(meth)

                        # Apply template Matching
                        res = cv2.matchTemplate(capture, template, method)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

                        # print(str(max_val))
                        if max_val > maxwkeittemp:
                            maxwkeittemp = max_val
                            maxnotemp = i
            print(str(maxnotemp))

    def _getCroppedBoxes(self, videostream):
        for image in videostream:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gauss = cv2.GaussianBlur(gray, (5, 5), 0)
            canny = cv2.Canny(gauss, 100, 200)

            contours, hierarchy = cv2.findContours(canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
            crops = []

            for i, cnt in enumerate(contours):
                if hierarchy[0][i][3] != -1 and hierarchy[0][i][2] < 0:
                    print("hir1")
                    if cv2.contourArea(cnt) > 100 and cv2.contourArea(cnt) < 3000:
                        print("hir2")
                        x, y, w, h = cv2.boundingRect(cnt)
                        if w < 50:
                            print("hir3")
                            if h < 100:
                                print("hir4")
                                if 0.35 < w / h < 0.7:
                                    print("hir5")
                                    box_classified = True
                                    rect = cv2.minAreaRect(cnt)
                                    box = cv2.boxPoints(rect)
                                    box = np.int0(box)
                                    for point in box:
                                        if point[0] == 0 or point[1] == 0:
                                            box_classified = False
                                    if box_classified:
                                        print(hierarchy[0][i])
                                        print(rect)
                                        print(box)
                                        print("--------------------")
                                        # Append to Crops
                                        x, y, width, height = cv2.boundingRect(box)
                                        crops.append(canny[y: y + height, x: x + width])
        return crops

    ###################################################################
    #Helper
    def SaveImageStreamToFS(self,imageStream):
        print("IPC: saving stream to FS...")
        cwd = os.getcwd()
        counter = 0
        for img in imageStream:
            frameString = cwd + "img_" + str(counter) + ".jpg".format()
            print(frameString)
            cv2.imwrite(frameString, img)
            counter += 1

    def _readTemplateArray(self, path):
        templateArray = []
        path = os.getcwd() + path
        for imgName in os.listdir(path):
            templateArray.append(path + imgName)

    def _setupGPIO(self):
        # Hier können die jeweiligen Eingangs-/Ausgangspins ausgewählt werden
        self._trigger_AusgangsPin = 17
        self._echo_EingangsPin = 27
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._trigger_AusgangsPin, GPIO.OUT)
        GPIO.setup(self._echo_EingangsPin, GPIO.IN)
        GPIO.output(self._trigger_AusgangsPin, False)

    def UnloadGPIO(self):
        GPIO.cleanup()