class DataController():
    def __init__(self, uartCommunicator):
        print("DC: Init DataController")
        self._uartCommunicator = uartCommunicator

        self._accelerationLenghtwiseList = []
        self._accelerationCrosswiseList = []
        self._speedData = []
        self._topSignalStream = []

    def StoreAccelerationLenghtwise(self, accelerationLenghtwise):
        self._accelerationLenghtwise.append(accelerationLenghtwise)

    def StoreAccelerationCrosswise(self, accelerationCrosswise):
        self._accelerationCrosswiseList.append(accelerationCrosswise)

    def StoreSpeedData(self, speedData):
        self._speedData.append(speedData)

    def SaveTopSignalStream(self, imagestream):
        self._topSignalStream.append(imagestream)

    def GetTopSingalStream(self):
        return self._topSignalStream

    def PersistData(self):
        print("DC: Persist acceleration Data")
        #todo in File schreiben