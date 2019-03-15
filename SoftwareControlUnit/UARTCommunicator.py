from SoftwareControlUnit import SoftwareControlUnit
from Thread.ParallelTask import ParallelTask
from Tasks.SpeedMeasurementTask import SpeedMeasurementTask
from time import sleep

class UARTCommunicator():
    _softwareControlUnit = None
    _dataController = None

    #Flags
    _isStarted = False
    _isCubeFound = False
    _isCubeReached = False
    _isCubeSafed = False
    _isTrainStopped = False

    _speedMeasurementThread = None

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
        self._speedMeasurementThread = ParallelTask(SpeedMeasurementTask())
        self._softwareControlUnit.Run()

    def SetDatacontroller(self, dataController):
        _dataController = dataController

    def StartSpeedMeasurement(self):
        print("UARTC: speed measurement started")
        self._speedMeasurementThread.Start()

    def StopSpeedMeasurement(self):
        print("UARTC: speed measurement started")
        self._speedMeasurementThread.Stop()

    ###################################################################
    # Speedcontrol

    def SetSpeed(self, speedAmmount):
        print("UARTC: speed set to: {}".format(speedAmmount))
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
        print("UARTC: safing Cube...")
        while not self._isCubeSafed:
            # todo
            sleep(0.1)
            self._isCubeSafed = True

    def StopAtNextSign(self):
        print("UARTC: stopping at next sign...")
        while not self._isTrainStopped:
            self._isTrainStopped = True
