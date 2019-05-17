#Import nextState
from Scripts.Behaviours.NextState import NextState

class DemoState():
    _stateMachine = None
    _isStopped = False

    def __init__(self, stateMachine):
		#Init with Statemachine Reference
        self._stateMachine = stateMachine

    def OnInit(self):
        pass

    def OnRun(self):
        #DoWork
        self._stateMachine.setNextState(NextState(self._stateMachine))
        self.Stop()

    def OnExit(self):
        pass

    def Stop(self):
        self._isStopped = True




