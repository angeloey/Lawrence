import serial

serialPort = serial.Serial(port = "COM10", baudrate=9600,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE) # setup serial port on pc

serialString = ""                                           # Used to hold data coming over UART
serialMessage = ""

def checkReady(): ## needs testing
    global serialMessage
    global serialString
    if(serialPort.in_waiting > 0):
        serialString = serialPort.readline()
        serialMessage = (serialString.decode('Ascii'))
        print(serialMessage)
        if("Ready" in serialMessage):
            return 1
        else:
            return 0
    elif("Ready" in serialMessage):
        return 1
    else:
        return 0

def waitForReady(): ## needs testing
    global serialMessage
    while (checkReady() == 0):
        pass
    serialMessage = "waiting for all clear"
    return

def raisePen():
    waitForReady()
    serialPort.write(b"penHIGH\r\n") ## implemented and tested in C  ## not tested as a function
    return

def lowerPen():
    waitForReady()
    serialPort.write(b"penLOW\r\n") ## implemented and tested in C  ## not tested as a function
    return

def forwards():
    waitForReady()
    serialPort.write(b"stepFWD\r\n") ## implemented and tested in C  ## not tested as a function
    return

def backwards():
    waitForReady()
    serialPort.write(b"stepBCK\r\n") ## implemented and tested in C  ## not tested as a function
    return





def turnR():
    waitForReady()
    serialPort.write(b"turnR\r\n") ## implemented and tested in C  ## not tested as a function
    return

def turnL():
    waitForReady()
    serialPort.write(b"turnL\r\n") ## implemented and tested in C  ## not tested as a function
    return

def stepFL():
    waitForReady()
    serialPort.write(b"stepFL\r\n") ## implemented and tested in C  ## not tested as a function
    return

def stepFR():
    waitForReady()
    serialPort.write(b"stepFR\r\n") ## implemented and tested in C  ## not tested as a function
    return

def stepBL():
    waitForReady()
    serialPort.write(b"stepBL\r\n") ## implemented and tested in C  ## not tested as a function
    return

def stepBR():
    waitForReady()
    serialPort.write(b"stepBR\r\n") ## implemented and tested in C  ## not tested as a function
    return