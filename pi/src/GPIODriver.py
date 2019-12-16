from gpiozero import LED
import time
import RPi.GPIO as GPIO



'''
Control GPIO pins.


Pin configuration and actions handled.

TODO- FeedCat is returning immediately, asynchronous call will be implemented.
'''


class GPIODriver:
    def __init__(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Initialize I/O constants
        # GPIO17 = Green Led #RGB PINS
        self._greenLedPin  = 17
        # GPIO22           = Red Led
        self._redLedPin    = 22
        # GPIO27           = Yellow Led
        self._yellowLedPin = 27
        # GPIO12           = PWM output Servo
        self._pwmPin       = 12
        # GPIO12           = Trig input Sonar
        self._sonartrigPin = 23
        # GPIO12           = Echo output Sonar
        self._sonarechoPin = 18


        # I/O objects
        self._greenLed  = LED(self._greenLedPin)
        self._redLed    = LED(self._redLedPin)
        self._yellowLed = LED(self._yellowLedPin)



        #setups of PWM inputs and outputs
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12,GPIO.OUT)
        p = GPIO.PWM(12,50)
        p.start(7.5)

        self._pwm  = p

    def greenLedOn(self):
        self._greenLed.on()

    def redLedOn(self):
        self._redLed.on()

    def yellowLedOn(self):
        self._yellowLed.on()

    def greenLedOff(self):
        self._greenLed.off()

    def redLedOff(self):
        self._redLed.off()

    def yellowLedOff(self):
        self._yellowLed.off()

    def openFoodGate(self):
        self._pwm.ChangeDutyCycle(12.5)


    def closeFoodGate(self):
        self._pwm.ChangeDutyCycle(2.5)

    def feedCat(self):
        self.openFoodGate()
        time.sleep(5)
        self.closeFoodGate()


    def sonarMeasure(self):
        '''
        !!! DO NOT USE
        TODO : NEED TIMEOUT FOR INFINITE LOOP
        '''

        GPIO.output(TRIG, False)
        time.sleep(1)
        GPIO.output(TRIG, True)
        time.sleep(1)
        GPIO.output(TRIG, False)


        pulse_start = 0
        while GPIO.input(ECHO) == 0 :
            pulse_start = time.time()


        pulse_end = 0
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()


        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        return distance
