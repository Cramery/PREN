import BlackBoard
#Import First State
from Scripts.Behaviours.Ready import Ready

class Agent():
    __nextState = None
    __currentState = None
    blackBoard = None

    def __init__(self):
        self.blackBoard = BlackBoard
		#Set First State(has to be imported)
        self.setNextState(Ready(self))
		#Run States until nextState is None
        while self.__nextState is not None:
            self.__currentState = self.__nextState
            self.__currentState.OnInit()
            self.__currentState.OnRun()
            self.__currentState.OnExit()
        print("State Machine finished")

    def setNextState(self, state):
        self.__nextState = state