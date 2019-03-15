from DataController import DataController
from ImageProcessingController import ImageProcessingController
from Thread.ParallelTask import ParallelTask


class SoftwareControlUnit():
    _dataController = None
    _imageProcessingController = None
    _uartCommunicator = None

    _stopSignCounter = 0
    _isTargetEvaluated = False
    _targetStopSignNumber = 0
    _isLookingForStopSign = False

    _SPEEDMAX = 20
    _CURVESPEED = 12
    _SEARCHSPEEDFAST = 10
    _SEARCHSPEEDSLOW = 5


    def __init__(self, uartCommunicator):
        print("SCU: Init SoftwareControllingUntit")
        self._uartCommunicator = uartCommunicator
        self._dataController = DataController(self, self._uartCommunicator)
        self._imageProcessingController = ImageProcessingController(self)
        self._uartCommunicator.SetDatacontroller(self._dataController)
        self._imageProcessingController.SetDatacontroller(self._dataController)

    def Run(self):
        print("SCU: Start")
        self._uartCommunicator.StartSpeedMeasurement()
        self._uartCommunicator.SetSpeed(self._SEARCHSPEEDFAST)
        self._uartCommunicator.LookForCube()
        self._uartCommunicator.SetSpeed(self._SEARCHSPEEDSLOW)
        self._uartCommunicator.ReachCube()
        self._uartCommunicator.SafeCube()
        self._uartCommunicator.SetSpeed(self._SPEEDMAX)
        self._imageProcessingController.StartLookingForCurves()
        self._imageProcessingController.LookForSigns()

    def OnSignFound(self, signData):
        #Evaluate StopsignNumber
        if not self._isTargetEvaluated and signData.SignType == 1:
            self._targetStopSignNumber = signData.NumberOnSign
            print("SCU: Sign number {} evaluated".format(self._targetStopSignNumber))
            self._isTargetEvaluated = True
        #Increase Stopshieldcounter if Shield is Stopshield
        if signData.ShieldType == 1:
            self._stopSignCounter += 1
        #If Stopshield is passed the 2nd time
        if signData.ShieldType == 1 and self._stopSignCounter == 2:
            self._imageProcessingController.StopLookingForCurves()
            self._uartCommunicator.SetSpeed(self._SEARCHSPEEDFAST)
            self._isLookingForStopSign = True
        #If Stopsign and is Looking for Stopsign
        if signData.SignType == 0 and self._isLookingForStopSign:
            self._uartCommunicator.SetSpeed(self._SEARCHSPEEDSLOW)
            self._isStopSignDetected = self._verifyStopSign(signData)
        #Is Stopsign was found
        if self._isStopSignDetected:
            self._uartCommunicator.StopAtNextSign()
            self._uartCommunicator.StopSpeedMeasurement()

    def OnCurveDetected(self):
        self._uartCommunicator.SetSpeed(self._CURVESPEED)

    def OnCurveLeft(self):
        self._uartCommunicator.SetSpeed(self._SPEEDMAX)

    def _verifyStopSign(self, sign):
        if sign.NumberOnShield == self._targetStopSignNumber:
            return True
        else:
            return False