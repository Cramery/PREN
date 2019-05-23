from collections import deque
import os

class DataController():
    def __init__(self, uartCommunicator):
        print("DC: Init DataController")
        self.uartCommunicator = uartCommunicator
        #Datacontainers
        self.accelerationLenghtwiseList = []
        self.accelerationCrosswiseList = []
        self.speedData = []
        self.topSignalStream = deque()
        self.allImagesList = []
        #PersistFilePath
        self._persistFileName = os.getcwd()+ '/data/data.txt'

    def StoreAccelerationLenghtwise(self, accelerationLenghtwise):
        self.accelerationLenghtwiseList.append(accelerationLenghtwise)

    def StoreAccelerationCrosswise(self, accelerationCrosswise):
        self.accelerationCrosswiseList.append(accelerationCrosswise)

    def StoreSpeedData(self, speedData):
        self.speedData.append(speedData)

    def SaveSignalStream(self, imagestream):
        for img in imagestream:
            self.topSignalStream.append(img)
            self.allImagesList.append(img)

    def GetImageFromSignalStream(self):
        if not self.SignalStreamIsEmpty:
            return self.topSignalStream.popleft()

    def SignalStreamIsEmpty(self):
        if len(self.topSignalStream) >= 1:
            return False
        else:
            return True

    def GetAllImages(self):
        return self.allImagesList

    def PersistData(self):
        print("DC: Persist acceleration Data")
        with open(self._persistFileName, 'w') as f:
            f.write("Speeddata:\n")
            f.write("-----------------------------------------------------\n")
            for item in self.speedData:
                f.write("%s\n" % item)
            f.write("-----------------------------------------------------\n")
            f.write("AccelerationLenghtwise:\n")
            f.write("-----------------------------------------------------\n")
            for item in self.accelerationLenghtwiseList:
                f.write("%s\n" % item)
            f.write("-----------------------------------------------------\n")
            f.write("AccelerationCrosswise:\n")
            f.write("-----------------------------------------------------\n")
            for item in self.accelerationCrosswiseList:
                f.write("%s\n" % item)