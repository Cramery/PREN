from DataController import DataController
from ImageProcessingController import  ImageProcessingController
from Thread.ParallelTask import ParallelTask
from Tasks.UARTListenerThread import UARTListenerThread
import serial
import threading

class UARTCommunicator():
    # Receive Commanddefinitions
    onCommand = "9"
    #Send Commanddefinitions
    successInit = b'1'
    roundsDriven = b'5'
    stopSignDetected = b'7'

    def __init__(self):
        print("UARTC: Init UARTCommunicator")
        self.dataController = DataController(self)
        self.imageProcessingController = ImageProcessingController(self, self.dataController)
        #Control
        self.isStarted = False
        #Serialport
        self.setupSerialPorts()
        #UART Listener Thread initialisieren
        self.startSigndetectionEvent = threading.Event()
        self.uartListenerThread = ParallelTask(UARTListenerThread(self.serialPortRx, self.dataController, self.startSigndetectionEvent))
        self.serialPortTx.write(self.successInit)
        self.startSigndetectionEvent.clear()

    def ListenForStart(self):
        print("UARTC: listening for ON-Signal")
        while not self.isStarted:
            rcv = self.serialPortRx.read(1).decode("utf-8")
            #todo löschen
            rcv = self.onCommand
            print("UARTC: listening...", rcv)
            #todo löschen -> Signal von Microcontroller
            #Signale für start, speed und accelerationmeasurement und start signdetection schreiben
            self.serialPortRx.write(b'9')
            self.serialPortRx.write(b'2')
            self.serialPortRx.write(b'101')
            self.serialPortRx.write(b'3')
            self.serialPortRx.write(b'202')
            self.serialPortRx.write(b'8')
            self.serialPortRx.write(b'303')
            self.serialPortRx.write(b'4')
            if(rcv == self.onCommand):
                print("UARTC: On-Signal detected")
                self.isStarted = True
        #UART Listener-Thread starten
        self.StartUARTListener()
        #Auf StartSignDetectionEvent warten
        self.startSigndetectionEvent.wait()
        self.StartSignDetection()

    def StartSignDetection(self):
        print("UARTC: Cube is safed")
        self.imageProcessingController.LookForStartSignCaptureStream()

    def LastRoundIsFinished(self):
        print("UARTC: Last round is finished")
        self.serialPortTx.write(self.roundsDriven)
        #todo self._playBuzzer(self._imageProcessingController.GetStopSignDigit())
        self.imageProcessingController.DetectStopSign()

    def StopTrain(self):
        print("UARTC: Next Sign is Stopsign")
        #self._serialPortTx.write(self._stopSignDetected)
        self.uartListenerThread.Stop()
        self.dataController.PersistData()
        self.imageProcessingController.UnloadGPIO()

    def _playBuzzer(self, count):
        #todo
        print("Buzzer sound: ", count)

    ###################################################################
    #UART-Listener
    def StartUARTListener(self):
        print("UARTC: UARTListener started")
        self.uartListenerThread.Start()

    def StopUARTListener(self):
        print("UARTC: UARTListener stopped")
        self.uartListenerThread.Stop()

    ###################################################################
    #Helpmethods

    def _listSerialPorts(self):
        ports = list(serial.port_list.comports())
        for p in ports:
            print(p)

    def setupSerialPorts(self):
        #todo serialPortTxPath = "/dev/ttyAMA0"
        serialPortRxPath = "/dev/ttyS0"
        serialPortTxPath = "/dev/ttyS0"
        baudrate = 9600
        serialtTimeout = 1.0
        self.serialPortRx = serial.Serial(serialPortRxPath, baudrate=baudrate, timeout=serialtTimeout)
        self.serialPortTx = serial.Serial(serialPortTxPath, baudrate=baudrate, timeout=serialtTimeout)