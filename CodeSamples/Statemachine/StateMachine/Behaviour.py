class Behaviour():
    _stateMachine = None
    _isStopped = False

    def __init__(self, stateMachine):
		#Set Reference to Statemachine -> Used for Blackboard and set next State dynamically
        self.__stateMachine = stateMachine

    def OnInit(self):
        pass

    def OnRun(self):
        pass

    def OnExit(self):
        pass

    def Stop(self):
        self.__isStopped = True