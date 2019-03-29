from DataController import DataController
from ImageProcessingController import  ImageProcessingController
from Thread.ParallelTask import ParallelTask
from Tasks.UARTListenerThread import UARTListenerThread
from time import sleep
import serial
import serial.tools.list_ports as port_list

class UARTCommunicator():
    _dataController = None
    _uartListenerThread = None

    #Serialport
    #todo _serialPortPath = "/dev/ttyAMA0"
    _serialPort = None
    _serialPortPath = ""
    _baudrate = 115200
    _serialtTimeout = 3.0

    #Flags
    _isStarted = False

    #Receive Commanddefinitions
    _onCommand = 0
    _accelerationLenghtwiseCommand = 2 # Es folgen 3 Byte Data
    _accelerationCrosswiseCommand = 3 # Es folgen 3 Byte Data
    _startSignDetectionCommand = 4

    #Send Commanddefinitions
    _successInit = 1
    _roundsDriven = 5
    _halteSignalRead = 6
    _stopSignDetected = 7

    def __init__(self):
        print("UARTC: Init UARTCommunicator")
        self._dataController = DataController(self)
        self._imageProcessingController = ImageProcessingController(self, self._dataController)
        self._serialPort = None
        #todo self.listSerialPorts()
        #todo self.setSerialPort()
        #todo port = serial.Serial(_serialPortPath, baudrate=_baudrate, timeout=_serialtTimeout)

    def ListenForStart(self):
        print("UARTC: listening for ON-Signal")
        while not self._isStarted:
            #todo rcv = port.read(8)
            rcv = 0
            if(rcv == self._onCommand):
                print("UARTC: On-Signal detected")
                self._isStarted = True
        #todo uartListener Thread mit port initialisieren
        self._uartListenerThread = ParallelTask(UARTListenerThread(self, self._serialPort))
        self.StartUARTListener()

    def CubeIsSafed(self):
        print("UARTC: Cube is safed")
        self._imageProcessingController.LookForHalteAndStartSign()

    def LastRoundIsFinished(self):
        print("UARTC: Last round is finished")
        #todo UART Singal senden
        self._imageProcessingController.LookForStopSign()

    def NextSignIsStopSign(self):
        print("UARTC: Next Sign is Stopsign")
        #todo UART Signal senden
        self._uartListenerThread.Stop()
        self._dataController.PersistData()

    ###################################################################
    #Listener
    def StartUARTListener(self):
        print("UARTC: UARTListener started")
        self._uartListenerThread.Start()

    def StopUARTListener(self):
        print("UARTC: UARTListener stopped")
        self._uartListenerThread.Stop()

    ###################################################################
    #Helpmethods

    def listSerialPort(self):
        ports = list(port_list.comports())
        for p in ports:
            print(p)

    def setSerialPort(self):
        ports = list(port_list.comports())
        if ports:
            _serialPortPath = ports[0]