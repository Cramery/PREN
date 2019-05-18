from DataController import DataController
from ImageProcessingController import  ImageProcessingController
from Thread.ParallelTask import ParallelTask
from Tasks.UARTListenerThread import UARTListenerThread
import serial
import threading
import RPi.GPIO as GPIO
from time import sleep

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
            print("UARTC: listening...", rcv)
            rcv = "9"
            #todo löschen -> Signal von Microcontroller
            #Signale für start, speed und accelerationmeasurement und start signdetection schreiben
            self.serialPortTx.write(b'9')
            self.serialPortTx.write(b'2')
            self.serialPortTx.write(b'101')
            self.serialPortTx.write(b'3')
            self.serialPortTx.write(b'202')
            self.serialPortTx.write(b'8')
            self.serialPortTx.write(b'303')
            self.serialPortTx.write(b'4')
            if(rcv == self.onCommand):
                print("UARTC: On-Signal detected")
                self.isStarted = True
        #UART Listener-Thread starten
        self.StartUARTListener()
        #Auf StartSignDetectionEvent warten
        #todo self.startSigndetectionEvent.wait()
        self.StartSignDetection()

    def StartSignDetection(self):
        print("UARTC: Cube is safed")
        self.imageProcessingController.LookForStartSignCaptureStream()

    def LastRoundIsFinished(self):
        print("UARTC: Last round is finished")
        self.serialPortTx.write(self.roundsDriven)
        stopsigndigit = self.imageProcessingController.GetStopSignDigit()
        self.__playBuzzer(stopsigndigit)
        self.imageProcessingController.DetectStopSign()

    def StopTrain(self):
        print("UARTC: Next Sign is Stopsign")
        #self._serialPortTx.write(self._stopSignDetected)
        self.uartListenerThread.Stop()
        self.dataController.PersistData()
        self.UnloadGPIO()
        self.closeSerialPorts()

    def __playBuzzer(self, number):
        print("Buzzer sound: ", number)
        self.buzzer.start(1)
        for x in range(number):
            sleep(1)
            self.buzzer.ChangeFrequency(1500)
            sleep(1)
            self.buzzerChangeFrequency(10)

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
        serialPortTxPath = "/dev/ttyAMA0"
        serialPortRxPath = "/dev/ttyS0"
        baudrate = 9600
        serialtTimeout = 1.0
        self.serialPortRx = serial.Serial(serialPortRxPath, baudrate=baudrate, timeout=serialtTimeout)
        self.serialPortTx = serial.Serial(serialPortRxPath, baudrate=baudrate, timeout=serialtTimeout)

    def closeSerialPorts(self):
        self.serialPortRx.close()
        self.serialPortTx.close()

    def setupGPIO(self):
        # Hier können die jeweiligen Eingangs-/Ausgangspins ausgewählt werden
        self.buzzer_Ausgangspin = 24
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_Ausgangspin, GPIO.OUT)
        self.buzzer = GPIO.PWM(self.buzzer_Ausgangspin, 10)

    def UnloadGPIO(self):
        GPIO.cleanup()