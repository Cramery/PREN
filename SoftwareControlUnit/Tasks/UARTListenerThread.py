import time

class UARTListenerThread():
    #Commands
    accelerationLenghtwiseCommand = [b'\x02\n'] # Es folgen 3 Byte Data
    accelerationCrosswiseCommand = [b'\x03\n'] # Es folgen 3 Byte Data
    speedCommand = [b'\x08\n'] # Es folgen 3 Byte Data
    startSignDetectionCommand = [b'\x04\n']

    def __init__(self, serialPort, datacontroller, startSigndetectionEvent):
        print("ULT: init")
        self.dataController = datacontroller
        self.serialPort = serialPort
        # Flag
        self.isStarted = True
        self.startSigndetectionEvent = startSigndetectionEvent

    def Run(self):
        print("ULT: running")
        while self.isStarted:
            rcv = self.serialPort.readlines(1)
            rcv = self.startSignDetectionCommand
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
            self.dataController.StoreAccelerationCrosswise(self.serialPort.readlines(1))
        elif argument == self.accelerationLenghtwiseCommand:
            print("ULT: acceleration Lenghtwise")
            self.dataController.StoreAccelerationLenghtwise(self.serialPort.readlines(1))
        elif argument == self.speedCommand:
            print("ULT: speed ")
            self.dataController.StoreSpeedData(self.serialPort.readlines(1))
        #else:
            #print("InvalidArgument passed:", argument)