class ImageProcessingController():
    _dataController = None
    _uartCommunicator = None

    _stopSignDigit = 0
    _startSignCounter = 0

    _isStopSignFound = False

    def __init__(self, uartCommunicator, dataController):
        print("IPC: Init ImageProcessingController")
        self._uartCommunicator = uartCommunicator
        self._dataController = dataController

    def LookForHalteAndStartSign(self):
        print("IPC: started looking for START and HALTE signs")
        while self._stopSignDigit == 0 and self._startSignCounter <= 3:
            #todo
            self._stopSignDigit = 3
            self._startSignCounter += 1
        print("IPC: 3 Rounds finished, Stopsigndigit is ".format(self._stopSignDigit))
        self._uartCommunicator.LastRoundIsFinished()

    def LookForStopSign(self):
        print("IPC: started looking for STOP signs")
        while not self._isStopSignFound:
            self._isStopSignFound = True
        print("IPC: Stop sign found")
        self._uartCommunicator.NextSignIsStopSign()
