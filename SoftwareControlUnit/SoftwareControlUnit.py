from DataController import DataController
from ImageProcessingController import ImageProcessingController
from UARTCommunicator import UARTCommunicator


class SoftwareControlUnit():
    _dataController = None
    _imageProcessingController = None
    _uartCommunicator = None

    _isStarted = False

    def __init__(self):
        self._uartCommunicator = UARTCommunicator(self)
        self._dataController = DataController(self, self._uartCommunicator)
        self._imageProcessingController = ImageProcessingController(self)


    def ListenForStart(self):
        print("Listening for ON signal")
        while not self._isStarted:
            #todo
            pass


