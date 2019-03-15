from SoftwareControlUnit import SoftwareControlUnit
#todo from Thread.ParallelTask import ParallelTask
from time import sleep

class UARTCommunicator():
    _softwareControlUnit = None
    _dataController = None

    #Flags
    _isStarted = False
    _isCubeFound = False
    _isCubeReached = False
    _isCubeSafed = False
    _isPossibleStopDetected = False

    _measurementThread = None

    def __init__(self):
        print("UARTC: Init UARTCommunicator")

    def ListenForStart(self):
        print("UARTC: listening for ON signal")
        while not self._isStarted:
            # todo
            print("UARTC: On-Signal detected")
            self._isStarted = True
        #SCU initialisieren und Start Methode starten
        self._softwareControlUnit = SoftwareControlUnit(self)
        self._softwareControlUnit.Start()

    def SetDatacontroller(self, dataController):
        _dataController = dataController

    def StartMeasurement(self):
        print("UARTC: measurement started")
        #self._measurementThread = ParallelTask(#todo TaskConstructor)

    ###################################################################
    # Speedcontrol

    def AddSpeed(self, speedAmmount):
        print("UARTC: add speed: {}".format(speedAmmount))
        #todo

    def ReduceSpeed(self, speedAmmount):
        print("UARTC: reduce speed: {}".format(speedAmmount))
        #todo

    def StopTrain(self):
        print("UARTC: Stop train")
        #todo

    ###################################################################
    # Detection & Grab

    def LookForCube(self):
        print("UARTC: look for Cube...")
        while not self._isCubeFound:
            # todo
            print("UARTC: Cube detected")
            self._isCubeFound = True

    def ReachCube(self):
        print("UARTC: Reaching Cube...")
        while not self._isCubeReached:
            # todo
            print("UARTC: Cube reached")
            self._isCubeReached = True
        self.StopTrain()

    def SafeCube(self):
        print("UARTC: Safing Cube...")
        while not self._isCubeSafed:
            # todo
            sleep(0.1)
            self._isCubeSafed = True

    def DetectPossibleStop(self):
        print("UARTC: detecting possible stop...")
        while not self._isPossibleStopDetected:
            # todo
            print("UARTC: possible reached")
            self._isPossibleStopDetected = True

