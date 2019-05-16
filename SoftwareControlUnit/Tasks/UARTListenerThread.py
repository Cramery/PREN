import time

class UARTListenerThread():
    #Commands
    _accelerationLenghtwiseCommand = "2" # Es folgen 3 Byte Data
    _accelerationCrosswiseCommand = "3" # Es folgen 3 Byte Data
    _speedCommand = "8" # Es folgen 3 Byte Data
    _startSignDetectionCommand = "4"

    def __init__(self, serialPort, datacontroller, startSigndetectionEvent):
        print("ULT: init")
        self._dataController = datacontroller
        self._serialPortRx = serialPort
        # Flag
        self._isStarted = True
        self._startSigndetectionEvent = startSigndetectionEvent

    def Run(self):
        print("ULT: running")
        while self._isStarted:
            rcv = self._serialPortRx.read(1).decode("utf-8")
            if rcv is not None:
                self.functionSwitch(rcv)

    def Stop(self):
        self._isStarted = False
        print("ULT: stopped")

    def functionSwitch(self, argument):
        if argument == self._startSignDetectionCommand:
            self._startSigndetectionEvent.set()
        elif argument == self._accelerationCrosswiseCommand:
            print("ULT: acceleration Crosswise ", self._serialPortRx.read(3).decode("utf-8"))
            #self._dataController.StoreAccelerationCrosswise(self._serialPortRx.read(3).decode("utf-8"))
        elif argument == self._accelerationLenghtwiseCommand:
            print("ULT: acceleration Lenghtwise ", self._serialPortRx.read(3).decode("utf-8"))
            #self._dataController.StoreAccelerationLenghtwise()
        elif argument == self._speedCommand:
            print("ULT: speed ", self._serialPortRx.read(3).decode("utf-8"))
            #self._dataController.StoreSpeedData(self._serialPortRx.read(3).decode("utf-8"))
        else:
            #print("InvalidArgument passed:", argument)
            pass