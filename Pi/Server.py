import threading
import socket
import time


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


    def receiveFrame(self):
        """
        1) Send a frame request
        2) Receive the newly captured frame
        3) Return Image object from PIL
        """

        # Image library...
        from PIL import Image

        # 1) frame request
        self._sendStr('receiveFrame')

        # 2) receive image
        print('Read length of the image...')
        uzunluk = int(self._clientsocket.recv(self._packageSize).decode())

        data = BytesIO()

        print('Reading total length ', uzunluk, ' bytes data...')
        for i in range(uzunluk // 4096 + 1):
            a = self._clientsocket.recv(self._packageSize)
            data.write(a)


        data.truncate(uzunluk)

        im = Image.open(data)


        print('Done!')
        return im


class CommandServer(Server):
    _serverName = 'CommandServer'

    def __init__(self, constants):
        self._listenPort    = constants['commandPort']
        self._packageSize   = constants['commandPackageSize']


        super().__init__(constants)
