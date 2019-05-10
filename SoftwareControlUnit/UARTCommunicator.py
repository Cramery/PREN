from DataController import DataController
from ImageProcessingController import  ImageProcessingController
from Thread.ParallelTask import ParallelTask
from Tasks.UARTListenerThread import UARTListenerThread
import serial

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
        self._setupSerialPorts()
        #self._serialPort.write(self._successInit)
        #Flag
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
        self._uartListenerThread = ParallelTask(UARTListenerThread(self, self._serialPortRx, self._dataController))
        self.StartUARTListener()

    def CubeIsSafed(self):
        print("UARTC: Cube is safed")
        self._imageProcessingController.LookForStartSignCaptureStream()

    def LastRoundIsFinished(self):
        print("UARTC: Last round is finished")
        #self._serialPortTx.write(self._roundsDriven)
        #todo self._playBuzzer(self._imageProcessingController.GetStopSignDigit())
        self._imageProcessingController.DetectStopSign()

    def StopTrain(self):
        print("UARTC: Next Sign is Stopsign")
        #self._serialPortTx.write(self._stopSignDetected)
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

    def _listSerialPorts(self):
        ports = list(serial.port_list.comports())
        for p in ports:
            print(p)

    def _setupSerialPorts(self):
        serialPortTxPath = "/dev/ttyAMA0"
        serialPortRxPath = "/dev/ttyS0"
        baudrate = 115200
        serialtTimeout = 1.0
        self._serialPortRx = serial.Serial(serialPortRxPath, baudrate=baudrate, timeout=serialtTimeout)
        self._serialPortTx = serial.Serial(serialPortTxPath, baudrate=baudrate, timeout=serialtTimeout)