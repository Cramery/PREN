from UARTCommunicator import UARTCommunicator

def main():
    print("Software started")
    _uartController = UARTCommunicator()
    _uartController.ListenForStart()

if __name__ == "__main__":
    main()