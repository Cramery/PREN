from UARTCommunicator import UARTCommunicator

def main():
    print("Software started")
    uartController = UARTCommunicator()
    uartController.ListenForStart()

if __name__ == "__main__":
    main()