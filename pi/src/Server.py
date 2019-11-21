import threading
import socket
import time

import logging

from io import BytesIO

import sys

class Server:

    def __init__(self, constants):
        self._listenAddress = constants['address']

        # Create socket
        self._serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._serversocket.bind((self._listenAddress, self._listenPort))

        # Current max. is only a single connection
        self._serversocket.listen(1)

        (clientsocket, address) = self._serversocket.accept()

        self._clientsocket  = clientsocket
        self._clientaddress = address

    def __del__(self):
        self._clientsocket.close()
        self._serversocket.close()


    def getAddress():
        return self._listenAddress

    def getPort():
        return self._listenPort

    def _sendStr(self, string):
        '''
        Send string with padded with blank spaces
        '''
        self._clientsocket.send((string + ' ' * (self._packageSize - len(string))).encode())



    def _receiveStr(self):
        '''
        Receive string terminated by blank spaces
        '''

        return self._clentsocket.recv(self._packageSize).decode().split()[0]



class VideoServer(Server):
    _serverName = 'VideoServer'

    def __init__(self, constants):
        self._listenPort    = constants['videoPort']
        self._packageSize   = constants['videoPackageSize']


        Server.__init__(self, constants)


    def receiveFrame(self, returnBytesIO=False):
        """
        1) Send a frame request
        2) Receive the newly captured frame
        3) Return Image object from PIL

        returnBytesIO=False : Set to true to get a BytesIO object instead of PIL Image
        """

        # Image library...
        from PIL import Image

        # 1) frame request
        self._sendStr('receiveFrame')

        # 2) receive image
        logging.info('Read length of the image...')
        uzunluk = int(self._clientsocket.recv(self._packageSize).decode())

        data = BytesIO()

        logging.info('Reading total length ' + str(uzunluk) + ' bytes data...')
        for i in range(uzunluk // 4096 + 1):
            a = self._clientsocket.recv(self._packageSize)
            data.write(a)


        data.truncate(uzunluk)

        if returnBytesIO:
            return data

        im = Image.open(data)


        logging.info('Done!')
        return im


class CommandServer(Server):
    _serverName = 'CommandServer'

    def __init__(self, constants):
        self._listenPort    = constants['commandPort']
        self._packageSize   = constants['commandPackageSize']


        super().__init__(constants)


    def greenLedOn(self):
        self._sendStr('greenLedOn')

    def redLedOn(self):
        self._sendStr('redLedOn')

    def greenLedOff(self):
        self._sendStr('greenLedOff')

    def redLedOff(self):
        self._sendStr('redLedOff')

    def allLedsOn(self):
        self.greenLedOn()
        self.redLedOn()

    def allLedsOff(self):
        self.greenLedOff()
        self.redLedOff()
