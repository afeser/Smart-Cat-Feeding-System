import threading
import socket
import time


from io import BytesIO

import sys

import logging
import threading

class Client:

    def __init__(self, constants):
        self._constants = constants
        self._destAddress = constants['address']

        # Create socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect
        self._socket.connect((self._destAddress, self._desPort))

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
        import CameraDriver
        self._desPort           = constants['videoPort']
        self._packageSize       = constants['videoPackageSize']
        self._fps               = constants['fps']
        self._frameSenderThread = None
        self._cameraDriver      = CameraDriver.CameraDriver()

        super().__init__(constants)

    def turnOnListenMode(self):
        '''
        Turn on listen mode by starting listener thread with a loop
        '''
        x = threading.Thread(target=self._turnOnListenMode)

        x.start()

    def _turnOnListenMode(self):
        '''
        Thread function for turnOnListenMode
        '''
        while True:
            self.listener()

    def listener(self, config=None):
        '''
        1) Listen for the new commands
        2) Do the corresponding command

        config=None : a list argument containing config for commands
        '''
        decider = self._receiveStr()

        if('receiveFrame' == decider):
            self._sendFrame(config[0])




    def _sendFrame(self, saveImage=None):
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
        imDat = cd.getImageData()

        if saveImage:
            f = open(saveImage, 'wb')

            f.write(imDat.getvalue())

            f.close()

        imDat.write(b'0' * (self._packageSize - int(cd.getImageDataSize()) % self._packageSize))
        socket.send(imDat.getvalue())





class CommandClient(Client):



    def __init__(self, constants):
        self._desPort         = constants['commandPort']
        self._packageSize     = constants['commandPackageSize']



        super().__init__(constants)

    def listenCommand(self):
        # Receive commands
        cmd = self._socket.recv(self._packageSize).decode()

        self._definedCommands[cmd]()
