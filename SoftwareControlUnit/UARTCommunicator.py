from DataController import DataController
from ImageProcessingController import  ImageProcessingController
from Thread.ParallelTask import ParallelTask
from Tasks.UARTListenerThread import UARTListenerThread
import serial
import threading

class UARTCommunicator():
    # Receive Commanddefinitions
    _onCommand = "9"
    #Send Commanddefinitions
    _successInit = b'1'
    _roundsDriven = b'5'
    _stopSignDetected = b'7'

    def __init__(self):
        print("UARTC: Init UARTCommunicator")
        self._dataController = DataController(self)
        self._imageProcessingController = ImageProcessingController(self, self._dataController)
        #Control
        self._isStarted = False
        #Serialport
        self._setupSerialPorts()
        #UART Listener Thread initialisieren
        self._startSigndetectionEvent = threading.Event()
        self._uartListenerThread = ParallelTask(UARTListenerThread(self._serialPortRx, self._dataController, self._startSigndetectionEvent))
        self._serialPortTx.write(self._successInit)
        self._startSigndetectionEvent.clear()

    def ListenForStart(self):
        print("UARTC: listening for ON-Signal")
        while not self._isStarted:
            rcv = self._serialPortRx.read(1).decode("utf-8")
            #todo löschen
            rcv = self._onCommand
            print("UARTC: listening...", rcv)
            #todo löschen -> Signal von Microcontroller
            #Signale für start, speed und accelerationmeasurement und start signdetection schreiben
            self._serialPortRx.write(b'9')
            self._serialPortRx.write(b'2')
            self._serialPortRx.write(b'101')
            self._serialPortRx.write(b'3')
            self._serialPortRx.write(b'202')
            self._serialPortRx.write(b'8')
            self._serialPortRx.write(b'303')
            self._serialPortRx.write(b'4')
            if(rcv == self._onCommand):
                print("UARTC: On-Signal detected")
                self._isStarted = True
        #UART Listener-Thread starten
        self.StartUARTListener()
        #Auf StartSignDetectionEvent warten
        self._startSigndetectionEvent.wait()
        self.StartSignDetection()

    def StartSignDetection(self):
        print("UARTC: Cube is safed")
        self._imageProcessingController.LookForStartSignCaptureStream()

    def LastRoundIsFinished(self):
        print("UARTC: Last round is finished")
        self._serialPortTx.write(self._roundsDriven)
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
    #UART-Listener
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
        #todo serialPortTxPath = "/dev/ttyAMA0"
        serialPortRxPath = "/dev/ttyS0"
        serialPortTxPath = "/dev/ttyS0"
        baudrate = 9600
        serialtTimeout = 1.0
        self._serialPortRx = serial.Serial(serialPortRxPath, baudrate=baudrate, timeout=serialtTimeout)
        self._serialPortTx = serial.Serial(serialPortTxPath, baudrate=baudrate, timeout=serialtTimeout)