from time import sleep

class Runnable():

    __Stop = False
    __threadName = None

    def __init__(self, threadName):
        self.__threadName = threadName

    def Run(self):
        while not self.__Stop:
            print (self.__threadName + " is Running")
            sleep(0.1)

    def Stop(self):
        print ("Stop Sred")
        self.__Stop = True;
