import SoftwareControlUnit

class ImageProcessingController():
    _softwareControlUnit = None
    _dataController = None

    def __init__(self, softwareControllUnit):
        print("IPC: Init ImageProcessingController")
        _softwareControlUnit = softwareControllUnit

    def SetDatacontroller(self, datacontroller):
        self._dataController = datacontroller

    def LookForSigns(self):
        print("IPC: Looking for Signs")
        #todo async

    def LookForCurves(self):
        print("IPC: Looking for Curves")
        #todo sync