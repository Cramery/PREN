class DataController():
    _uartCommunicator = None
    _accelerationLenghtwiseList = []
    _accelerationCrosswiseList = []

    def __init__(self, uartCommunicator):
        print("DC: Init DataController")
        _uartCommunicator = uartCommunicator

    def StoreAccelerationLenghtwise(self, accelerationLenghtwise):
        self._accelerationLenghtwise.append(accelerationLenghtwise)

    def StoreAccelerationCrosswise(self, accelerationCrosswise):
        self._accelerationCrosswiseList.append(accelerationCrosswise)

    def PersistData(self):
        print("DC: Persist acceleration Data")