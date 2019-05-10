from time import sleep

class UARTListenerThread():
    #Commands
    _accelerationLenghtwiseCommand = 2 # Es folgen 3 Byte Data
    _accelerationCrosswiseCommand = 3 # Es folgen 3 Byte Data
    _speedCommand = 8
    _startSignDetectionCommand = 4


    def __init__(self, uartCommunicator, serialPort, datacontroller):
        print("ULT: init")
        self._uartCommunicator = uartCommunicator
        self._dataController = datacontroller

        self._serialPort = serialPort
        # Flag
        self._isStarted = True

    def SetDatacontroller(self, datacontroller):
        self._dataController = datacontroller

    def Run(self):
        print("ULT: running")
        while self._isStarted:
            '''
            rcv = None
            rcv = self._serialPort.read(1) #one byte
            '''
            rcv = 4
            if rcv is not None:
                self.functionSwitch(rcv)
            sleep(2)

    def Stop(self):
        self._isStarted = False
        print("ULT: stopped")

    def functionSwitch(self, argument):
        if argument == self._accelerationLenghtwiseCommand:
            print("ULT: acceleration Lenghtwise")
            #self._dataController.StoreAccelerationLenghtwise(self._serialPort.read(3))
        elif argument == self._accelerationCrosswiseCommand:
            print("ULT: acceleration Crosswise")
            #self._dataController.StoreAccelerationCrosswise(self._serialPort.read(3))
        elif argument == self._speedCommand:
            print("ULT: speed")
            #self._dataController.StoreSpeedData(self._serialPort.read(3))
        elif argument == self._startSignDetectionCommand:
            self._uartCommunicator.CubeIsSafed()
        else:
            print("InvalidArgument passed")