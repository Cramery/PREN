from DataController import DataController
from ImageProcessingController import  ImageProcessingController
from Thread.ParallelTask import ParallelTask
from Tasks.UARTListenerThread import UARTListenerThread
import serial.tools.list_ports as port_list

class UARTCommunicator():
    # Receive Commanddefinitions
    _onCommand = 0
    #Send Commanddefinitions
    _successInit = 1
    _roundsDriven = 5
    #todo _halteSignalRead = 6 je nach dem ob wir postprocessing machen oder nicht
    _stopSignDetected = 7

    def __init__(self):
        print("UARTC: Init UARTCommunicator")
        self._dataController = DataController(self)
        self._imageProcessingController = ImageProcessingController(self, self._dataController)
        self._uartListenerThread = None
        # Serialport
        # todo self._serialPortPath = "/dev/ttyAMA0"
        self._serialPort = None
        self._serialPortPath = ""
        self._baudrate = 115200
        self._serialtTimeout = 3.0
        #todo self.listSerialPorts()
        #self.setSerialPort()
        #port = serial.Serial(_serialPortPath, baudrate=_baudrate, timeout=_serialtTimeout)
        #self._serialPort.write(self._successInit)
        # Flag
        self._isStarted = False

    def ListenForStart(self):
        print("UARTC: listening for ON-Signal")
        while not self._isStarted:
            #todo rcv = port.read(1)
            rcv = 0
            if(rcv == self._onCommand):
                print("UARTC: On-Signal detected")
                self._isStarted = True
        #todo uartListener Thread mit port initialisieren
        self._uartListenerThread = ParallelTask(UARTListenerThread(self, self._serialPort, self._dataController))
        self.StartUARTListener()

    def CubeIsSafed(self):
        print("UARTC: Cube is safed")
        self._imageProcessingController.LookForStartSignCaptureStream()

    def LastRoundIsFinished(self):
        print("UARTC: Last round is finished")
        #self._serialPort.write(self._roundsDriven)
        #todo self._playBuzzer(self._imageProcessingController.GetStopSignDigit())
        self._imageProcessingController.DetectStopSign()

    def StopTrain(self):
        print("UARTC: Next Sign is Stopsign")
        #self._serialPort.write(self._stopSignDetected)
        self._uartListenerThread.Stop()
        self._dataController.PersistData()
        self._imageProcessingController.UnloadGPIO()

    def _playBuzzer(self, count):
        #todo
        print("Buzzer sound: ", count)

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