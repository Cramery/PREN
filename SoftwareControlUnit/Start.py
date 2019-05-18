from UARTCommunicator import UARTCommunicator

def main():
    print("Software started")
    UARTCommunicator().ListenForStart()

if __name__ == "__main__":
    main()