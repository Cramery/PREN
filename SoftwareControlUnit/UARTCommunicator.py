﻿from DataController import DataController
from ImageProcessingController import  ImageProcessingController
from Thread.ParallelTask import ParallelTask
from Tasks.UARTListenerThread import UARTListenerThread
import serial
import threading
import RPi.GPIO as GPIO
from time import sleep

class UARTCommunicator():
    # Receive Commanddefinitions
    onCommand = [b'\t\n'] # =9
    #Send Commanddefinitions
    successInit = b'1\n'
    roundsDriven = b'5\n'
    stopSignDetected = b'7\n'

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
        self.uartListenerThread = ParallelTask(UARTListenerThread(self.serialPort, self.dataController, self.startSigndetectionEvent))
        self.serialPort.write(self.successInit)
        self.startSigndetectionEvent.clear()

    def ListenForStart(self):
        print("UARTC: listening for ON-Signal")
        while not self.isStarted:
            rcv = self.serialPort.readlines(1)
            print(rcv)
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
        self.serialPort.write(self.roundsDriven)
        #stopsigndigit = self.imageProcessingController.GetStopSignDigit()
        #self.__playBuzzer(stopsigndigit)
        self.imageProcessingController.DetectStopSign()

    def StopTrain(self):
        print("UARTC: Next Sign is Stopsign")
        self.serialPort.write(self.stopSignDetected)
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
        serialPortRxPath = "/dev/ttyS0"
        baudrate = 115200
        serialtTimeout = 1.0
        self.serialPort = serial.Serial(serialPortRxPath, baudrate=baudrate, timeout=serialtTimeout)

    def closeSerialPorts(self):
        self.serialPort.close()

    def setupGPIO(self):
        # Hier können die jeweiligen Eingangs-/Ausgangspins ausgewählt werden
        self.buzzer_Ausgangspin = 24
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_Ausgangspin, GPIO.OUT)
        self.buzzer = GPIO.PWM(self.buzzer_Ausgangspin, 10)

    def UnloadGPIO(self):
        GPIO.cleanup()