from threading import Thread

class ParallelTask:
    __runable = None
    __thread = None
    __isRunning = False

    def __init__(self, runable):
        self.__runable = runable
        self.__thread = Thread(target=self.__runable.Run)

    def Start(self):
        if not self.__isRunning:
            self.__isRunning = True
            self.__thread.start()

    def Stop(self):
        self.__runable.Stop()
        self.__isRunning = False



