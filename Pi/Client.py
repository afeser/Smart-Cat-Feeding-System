import threading
import socket
import time


from io import BytesIO

import sys

class Client:

    def __init__(self, constants):
        self._constants = constants
        self._destAddress = constants['address']

        # Create socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect
        self._socket.connect((self._destAddress, self._desPort))

    def sendStr(self):
        '''
        Send string with padded with blank spaces
        '''
        self._socket.send((string + ' ' * (string._packageSize - len(size))).encode())



    def receiveStr(self, string):
        '''
        Receive string terminated by blank spaces
        '''

        return self._socket.recv(self._packageSize).decode().split()[0]


class VideoClient(Client):

    def __init__(self, constants):
        import CameraDriver
        self._desPort           = constants['videoPort']
        self._packageSize       = constants['videoPackageSize']
        self._fps               = constants['fps']
        self._frameSenderThread = None
        self._cameraDriver      = CameraDriver.CameraDriver()

        super().__init__(constants)

    def listener(self):
        '''
        1) Listen for the new commands
        2) Do the corresponding command
        '''
        pass



    def startFrameSender(self):
        # Start frame sender thread
        # save the thread to kill later on request
        self._startFrameSender()

    def _startFrameSender(self):
        """
        First send the buffer size, then send the data
        """
        cd     = self._cameraDriver
        socket = self._socket
        while True:
            # or wait for the transfer...
            waitDuration = 1. / self._fps / 2

            # Capture
            cd.capture(waitDuration)

            # Send total size
            size = cd.getImageDataSize()
            socket.send((size + ' ' * (self._packageSize - len(size))).encode())

            # Send the file
            # Veriyi küçük boyutun tam katı yap
            imDat = cd.getImageData()
            imDat.write(b'0' * (self._packageSize - int(cd.getImageDataSize()) % self._packageSize))
            socket.send(imDat.getvalue())


class CommandClient(Client):



    def __init__(self, constants):
        self._desPort         = constants['commandPort']
        self._packageSize     = constants['commandPackageSize']

        # Server - Client commands
        self._definedCommands = {
            ('sayHello' + ' ' * (self._packageSize - len('sayHello'))) : self._sayHello
        }

        super().__init__(constants)

    def listenCommand(self):
        # Receive commands
        cmd = self._socket.recv(self._packageSize).decode()

        self._definedCommands[cmd]()


    # Commands...
    def _sayHello(self):
        print('Naber Cinim??')
