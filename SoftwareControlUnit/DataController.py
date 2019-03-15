class DataController():
    _softwareControlUnit = None
    _uartCommunicator = None

    _signList = []
    _signListIndex = 0

    _speedList = []
    _speedListIndex = 0

    def __init__(self, softwareControllUnit, uartCommunicator):
        print("DC: Init DataController")
        _softwareControlUnit = softwareControllUnit
        _uartCommunicator = uartCommunicator

    def SignDetected(self, signData):
        print("DC: Shield stored")
        self._softwareControlUnit.OnSignFound(signData)

    def SafeSignData(self, signData):
        self._signList[self._signListIndex] = signData
        self._signListIndex += 1

    def SafeSpeedData(self, speedData):
        self._speedList[self._speedListIndex] = speedData
        self._speedListIndex += 1

    def GetSignData(self):
        return self._signList

    def GetSpeedData(self):
        return self._speedList

