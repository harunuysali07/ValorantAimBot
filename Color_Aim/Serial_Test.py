import serial

serialPort = serial.Serial(port = "COM9", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

while(1):

        # Tell the device connected over the serial port that we recevied the data!
        # The b at the beginning is used to indicate bytes!
        serialPort.write(b"5| \r\n")