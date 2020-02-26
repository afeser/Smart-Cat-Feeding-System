import threading
import socket
import time


from io import BytesIO

import sys

import logging
import threading


import CameraDriver
import GPIODriver

class Client:

    def __init__(self, constants):
        self._constants = constants
        self._destAddress = constants['address']

        # Create socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect
        self._socket.connect((self._destAddress, self._desPort))

    def __del__(self):
        self._socket.close()

    def _sendStr(self, string):
        '''
        Send string with padded with blank spaces
        '''
        self._socket.send((string + ' ' * (self._packageSize - len(string))).encode())



    def _receiveStr(self):
        '''
        Receive string terminated by blank spaces
        '''

        return self._socket.recv(self._packageSize).decode().split()[0]


class VideoClient(Client):

    def __init__(self, constants):
        self._desPort           = constants['videoPort']
        self._packageSize       = constants['videoPackageSize']
        self._frameSenderThread = None
        self._cameraDriver      = CameraDriver.CameraDriver()

        super().__init__(constants)

    def turnOnListenMode(self):
        '''
        Turn on listen mode by starting thread with a loop
        '''
        x = threading.Thread(target=self._turnOnListenMode)

        x.start()

    def _turnOnListenMode(self):
        '''
        Thread function for turnOnListenMode
        '''
        while True:
            self.listenCommand()

    def listenCommand(self, config=None):
        '''
        1) Listen for the new commands
        2) Do the corresponding command

        config=None : a list argument containing config for commands
        '''
        decider = self._receiveStr()

        if('receiveFrame' == decider):
            if config:
                self._sendFrame(config[0])
            else:
                self._sendFrame()




    def _sendFrame(self, saveImage=False):
        '''
        First send the buffer size, then send the data.
        Return the sent frame data.

        saveImage=None : Give file name to save captured image - Test

        Do not use directly, correspondence is not exact with receiveFrame in Server.py
        '''
        cd     = self._cameraDriver
        socket = self._socket

        # Capture
        cd.capture()
        # Send total size
        size = cd.getImageDataSize()
        socket.send((size + ' ' * (self._packageSize - len(size))).encode())

        # Send the file
        logging.info('Sending file with size ' + str(size))
        imDat = cd.getImageData()

        if saveImage:
            f = open('savedImaged.jpg', 'wb')

            f.write(imDat.getvalue())

            f.close()

        imDat.write(b'0' * (self._packageSize - int(cd.getImageDataSize()) % self._packageSize))
        socket.send(imDat.getvalue())





class CommandClient(Client):



    def __init__(self, constants):
        self._desPort         = constants['commandPort']
        self._packageSize     = constants['commandPackageSize']

        self._GPIOController  = GPIODriver.GPIODriver()

        super().__init__(constants)

    def listenCommand(self):
        # Receive commands
        cmd  = self._receiveStr()
        gpio = self._GPIOController

        logging.info('Received command ' + str(cmd))
        #   # LEDs
        if cmd == 'greenLedOn':
            gpio.greenLedOn()
        elif cmd == 'redLedOn':
            gpio.redLedOn()
        elif cmd == 'yellowLedOn':
            gpio.yellowLedOn()
        elif cmd == 'greenLedOff':
            gpio.greenLedOff()
        elif cmd == 'redLedOff':
            gpio.redLedOff()
        elif cmd == 'yellowLedOff':
            gpio.yellowLedOff()

            # Food stuff...
        elif cmd == 'openFoodGate':
            gpio.openFoodGate()
        elif cmd == 'closeFoodGate':
            gpio.closeFoodGate()
        elif cmd == 'feedCat':
            amount = cmd._receiveStr()
            try:
                gpio.feedCat(int(amount))
            except:
                logging.warning('Can not decode amount of the food "' + amount + '"\nNot feeding cat...')

            # WTF are u saying??
        else:
            logging.warning('Meaningless command from server')



    def turnOnListenMode(self):
        '''
        Turn on listen mode by starting thread with a loop
        '''
        x = threading.Thread(target=self._turnOnListenMode)

        x.start()


    def _turnOnListenMode(self):
        while True:
            self.listenCommand()
