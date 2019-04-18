class DataController():
    def __init__(self, uartCommunicator):
        print("DC: Init DataController")
        self._uartCommunicator = uartCommunicator

        self._accelerationLenghtwiseList = []
        self._accelerationCrosswiseList = []

    def StoreAccelerationLenghtwise(self, accelerationLenghtwise):
        self._accelerationLenghtwise.append(accelerationLenghtwise)

    def StoreAccelerationCrosswise(self, accelerationCrosswise):
        self._accelerationCrosswiseList.append(accelerationCrosswise)

    def PersistData(self):
        print("DC: Persist acceleration Data")