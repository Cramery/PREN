from time import sleep
from Thread.ParallelTask import ParallelTask
from Tasks.LookForCurveTask import LookForCurveTask

class ImageProcessingController():
    _softwareControlUnit = None
    _dataController = None
    _lookingForCurveTask = None

    def __init__(self, softwareControllUnit):
        print("IPC: Init ImageProcessingController")
        self._softwareControlUnit = softwareControllUnit
        self._lookingForCurveTask = ParallelTask(LookForCurveTask())

    def SetDatacontroller(self, datacontroller):
        self._dataController = datacontroller

    def LookForSigns(self):
        print("IPC: started looking for Signs")
        while True:
            #todo Bildverarbeitung
            #signData =
            #self._dataController.SignDetected(signData)
            #self._softwareControlUnit.OnSignFound(signData)
            sleep(0.01)

    def StartLookingForCurves(self):
        print("IPC: started looking for Curves")
        self._lookingForCurveTask.Start()

    def StopLookingForCurves(self):
        print("IPC: stopped looking for Curves")
        self._lookingForCurveTask.Stop()