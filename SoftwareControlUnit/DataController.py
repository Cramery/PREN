class DataController():
    def __init__(self, uartCommunicator):
        print("DC: Init DataController")
        self._uartCommunicator = uartCommunicator
        #Datacontainers
        self._accelerationLenghtwiseList = []
        self._accelerationCrosswiseList = []
        self._speedData = []
        self._topSignalStream = []
        #PersistFilePath
        self._persistFileName = 'your_file.txt'


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
        '''
        with open(self._persistFileName, 'w') as f:
            f.write("Speeddata:\n")
            for item in self._speedData:
                f.write("%s\n" % item)
            f.write("AccelerationLenghtwise:\n")
            for item in self._accelerationLenghtwiseList:
                f.write("%s\n" % item)
            f.write("AccelerationCrosswise:\n")
            for item in self._accelerationCrosswiseList:
                f.write("%s\n" % item)
        '''