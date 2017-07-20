import time
# libraries to send data to Serial port
import serial
import struct
#define serial port
usbport = '/dev/ttyUSB0'
serialArduino = serial.Serial(usbport, 9600, timeout=1)

def moveMotor():
    serialArduino.write(b'w') #Move Forward
    serialArduino.readline()  #Read The executed Command from arduino
    time.sleep(0.5)
    serialArduino.write(b'x') #stop
    serialArduino.readline()  #Read The executed Command from arduino
    
    serialArduino.write(b'a') #Move Left
    serialArduino.readline()  #Read The executed Command from arduino
    time.sleep(0.5)
    serialArduino.write(b'x') #stop
    serialArduino.readline()  #Read The executed Command from arduino
    
    serialArduino.write(b'd') #Move Right
    serialArduino.readline()  #Read The executed Command from arduino
    time.sleep(0.5)
    serialArduino.write(b'x') #stop
    serialArduino.readline()  #Read The executed Command from arduino

    serialArduino.write(b's') #Move Back
    serialArduino.readline()  #Read The executed Command from arduino
    time.sleep(0.5)
    serialArduino.write(b'x') #stop
    serialArduino.readline()  #Read The executed Command from arduino

    serialArduino.write(b'l') #Head Move left
    serialArduino.readline()  #Read The executed Command from arduino
    time.sleep(0.5)
    serialArduino.write(b'x') #stop
    serialArduino.readline()  #Read The executed Command from arduino

    serialArduino.write(b'r') #Head Move Right
    serialArduino.readline()  #Read The executed Command from arduino
    time.sleep(0.5)
    serialArduino.write(b'x') #stop
    serialArduino.readline()  #Read The executed Command from arduino

moveMotor()
    
    
    
