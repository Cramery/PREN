import time

class UARTListenerThread():
    #Commands
    accelerationLenghtwiseCommand = "2" # Es folgen 3 Byte Data
    accelerationCrosswiseCommand = "3" # Es folgen 3 Byte Data
    speedCommand = "8" # Es folgen 3 Byte Data
    startSignDetectionCommand = "4"

    def __init__(self, serialPort, datacontroller, startSigndetectionEvent):
        print("ULT: init")
        self.dataController = datacontroller
        self.serialPortRx = serialPort
        # Flag
        self.isStarted = True
        self.startSigndetectionEvent = startSigndetectionEvent

    def Run(self):
        print("ULT: running")
        while self.isStarted:
            rcv = self.serialPortRx.read(1).decode("utf-8")
            if rcv is not None:
                self.functionSwitch(rcv)

    def Stop(self):
        self.isStarted = False
        print("ULT: stopped")

    def functionSwitch(self, argument):
        if argument == self.startSignDetectionCommand:
            self.startSigndetectionEvent.set()
        elif argument == self.accelerationCrosswiseCommand:
            print("ULT: acceleration Crosswise ")
            self.dataController.StoreAccelerationCrosswise(self.serialPortRx.read(3).decode("utf-8"))
        elif argument == self.accelerationLenghtwiseCommand:
            print("ULT: acceleration Lenghtwise")
            self.dataController.StoreAccelerationLenghtwise(self.serialPortRx.read(3).decode("utf-8"))
        elif argument == self.speedCommand:
            print("ULT: speed ")
            self.dataController.StoreSpeedData(self.serialPortRx.read(3).decode("utf-8"))
        #else:
            #print("InvalidArgument passed:", argument)