import serial

class UARTListenerThread():
    _serialPort = None
    _uartCommunicator = None

    #Flags
    _isStarted = True
    _isCubeSafed = False

    def __init__(self, uartCommunicator, serialPort):
        print("ULT: init")
        self._uartCommunicator = uartCommunicator
        self._serialPort = serialPort


    def Run(self):
        print("ULT: running")
        while self._isStarted:
            #todo acceleration measurement
            while not self._isCubeSafed:
                self._uartCommunicator.CubeIsSafed()
                self._isCubeSafed = True

    def Stop(self):
        self._isStarted = False
        print("ULT: stopped")
