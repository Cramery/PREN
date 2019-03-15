import SoftwareControlUnit

class DataController():
    _softwareControlUnit = None
    _uartCommunicator = None
    #todo find and define data structures & formats

    def __init__(self, softwareControllUnit, uartCommunicator):
        print("Init DataController")
        _softwareControlUnit = softwareControllUnit
        _uartCommunicator = uartCommunicator

    def SignDetected(self, signData):
        #todo
        pass

    def SafeMeasureData(self, measureData):
        #todo
        pass

    def GetSignData(self):
        #todo
        pass

    def GetSpeedData(self):
        #todo
        pass

