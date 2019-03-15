from DataController import DataController
from ImageProcessingController import ImageProcessingController



class SoftwareControlUnit():
    _dataController = None
    _imageProcessingController = None
    _uartCommunicator = None

    _speedMax = 20;


    def __init__(self, uartCommunicator):
        print("SCU: Init SoftwareControllingUntit")
        self._uartCommunicator = uartCommunicator
        self._dataController = DataController(self, self._uartCommunicator)
        self._imageProcessingController = ImageProcessingController(self)
        self._uartCommunicator.SetDatacontroller(self._dataController)
        self._imageProcessingController.SetDatacontroller(self._dataController)

    def Start(self):
        print("SCU: Start")
        self._uartCommunicator.StartMeasurement()
        self._uartCommunicator.AddSpeed(10)
        self._uartCommunicator.LookForCube()
        self._uartCommunicator.ReduceSpeed(5)
        self._uartCommunicator.ReachCube()
        self._uartCommunicator.SafeCube()
        self._uartCommunicator.AddSpeed(self._speedMax)
        self._imageProcessingController.LookForSigns()
        self._imageProcessingController.LookForCurves()

    def VerifyTarget(self):
        #todo async
        pass

    def OnCurveFound(self):
        #todo
        pass

    def OnCurveLeft(self):
        #todo
        pass





