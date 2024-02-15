import serial
from SerialCommands import *

serialPort.write(b"penLOW\r\n")
for i in range(3600):
    forwards()