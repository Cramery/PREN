from SoftwareControlUnit import SoftwareControlUnit
from Thread.ParallelTask import ParallelTask
from Tasks.SpeedMeasurementTask import SpeedMeasurementTask
from time import sleep
import serial
import serial.tools.list_ports as port_list

class UARTCommunicator():
    _softwareControlUnit = None
    _dataController = None

    #Serialport
    #_serialPortPath = "/dev/ttyAMA0"
    _serialPortPath = ""
    _baudrate = 115200
    _serialtTimeout = 3.0

    #Flags
    _isStarted = False
    _isCubeFound = False
    _isCubeReached = False
    _isCubeSafed = False
    _isTrainStopped = False

    _speedMeasurementThread = None

    def __init__(self):
        print("UARTC: Init UARTCommunicator")
        self.listSerialPorts()
        #todo self.setSerialPort()
        #port = serial.Serial(_serialPortPath, baudrate=_baudrate, timeout=_serialtTimeout)


    def ListenForStart(self):
        print("UARTC: listening for ON signal")
        while not self._isStarted:
            #todo rcv = port.read()
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

    ###################################################################
    #Helptools
    def listSerialPort(self):
        ports = list(port_list.comports())
        for p in ports:
            print(p)

    def setSerialPort(self):
        ports = list(port_list.comports())
        if ports:
            _serialPortPath = ports[0]