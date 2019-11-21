from gpiozero import LED
from time import sleep



'''
Control GPIO pins.


Pin configuration and actions handled.
'''

class GPIODriver:
    def __init__(self):
        # Initialize I/O constants
        # GPIO0 = Green Led
        self._greenLedPin = 0
        # GPIO2 = Red Led
        self._redLedPin   = 2



        # I/O objects
        self._greenLed = LED(self._greenLedPin)
        self._redLed   = LED(self._redLedPin)

    def greenLedOn(self):
        self._greenLed.on()

    def redLedOn(self):
        self._redLed.on()

    def greenLedOff(self):
        self._greenLed.off()

    def redLedOff(self):
        self._redLed.off()
