import threading

class ImageProcessorThread(threading.Thread):
    def __init__(self, owner):
        super(ImageProcessorThread, self).__init__()
        self.isTerminated = False
        self.isStopSignFound = True
        self.owner = owner
        self.start()
        print("IPCT: Image Processing Thread started")

    def run(self):
        while not self.isTerminated:
            while not self.isStopSignFound:
                print("IPCT: Processing Stream")
                for img in self.imagestream:
                    self._checkStartSignal(img)
                    if self.isStopSignFound:
                        self.owner.StartSignCounter += 1
                        break

    def SetImageStreamAndStart(self, imagestream):
        self.imagestream = imagestream
        self.isStopSignFound = False

    def FinishThread(self):
        print("IPCT: Image Processing Thread stopped")
        self.isTerminated = True

    def _checkStartSignal(self, img):
        pass
        self.isStopSignFound = True