import SoftwareControlUnit

class DataController():
    _softwareControlUnit = None
    _uartCommunicator = None

    def __init__(self, softwareControllUnit, uartCommunicator):
        _softwareControlUnit = softwareControllUnit
        _uartCommunicator = uartCommunicator