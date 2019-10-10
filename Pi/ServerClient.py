# Server-Client code for data and command stream
# In case of high performance, no C code will be needed

# Source(s) :
# https://docs.python.org/2/howto/sockets.html
# https://stackoverflow.com/questions/21233340/sending-string-via-socket-python


# Definitions :
# 1) Sometimes it is confusing that which side is server. Usually streaming side
# is assumed to be the server. However, in this configuration to clearly define
# the virtual machine server, server always refer to virtual machine.
#    Server : virtual machine server
#    Client : raspberry pi


# TODO(s)
# 1) Error-Handling
# 2) Logging
# 3) Connection lost-reconnection

import threading
import socket
import time


from io import BytesIO

import sys



# import logging

constants = {
    # Some constants both for server and client
    "address"   : 'localhost',
    'videoPort' : 10004,
    'commandPort' : 10007,

    ### To be optimized...

    # _videoPackageSize : package size that stream read is done per receive request
    # To be optimized for performance. Used in stream server.
    'videoPackageSize' : 4096,
    # _commandPackageSize : package size that stream read is done per receive request
    # Not need to be optimized, already small data stream.
    'commandPackageSize' : 1024,

    # Frame per second, how many frames will the client send in sendFrame mode
    # Moreover, it can be dynamic in the future depending on the vision algorithm
    # Notice increasing fps results in overflow in socket buffer...
    # Either a new technique will be used, or greater fps values will be avoided
    'fps' : 1

}


class Server:

    def __init__(self):
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



class VideoServer(Server):
    _serverName = 'VideoServer'

    def __init__(self):
        self._listenPort    = constants['videoPort']
        self._packageSize   = constants['videoPackageSize']


        Server.__init__(self)


    def receiveFrame(self):
        # Image library...
        from PIL import Image

        """
        Read a single image from the stream
        Return the Image object from PIL
        """

        # read length
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

    def __init__(self):
        self._listenPort    = constants['commandPort']
        self._packageSize   = constants['commandPackageSize']


        super().__init__()


    def sendCommand(self, cmd):
        # Determine the command, do the required actions!
        # This method is called from a main program
        self._clientsocket.send(cmd)


class Client:

    def __init__(self):
        self._destAddress = constants['address']

        # Create socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect
        self._socket.connect((self._destAddress, self._desPort))



class VideoClient(Client):

    def __init__(self):
        import CameraDriver
        self._desPort           = constants['videoPort']
        self._packageSize       = constants['videoPackageSize']
        self._fps               = constants['fps']
        self._frameSenderThread = None
        self._cameraDriver      = CameraDriver.CameraDriver()

        super().__init__()

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



    def __init__(self):
        self._desPort         = constants['commandPort']
        self._packageSize     = constants['commandPackageSize']

        # Server - Client commands
        self._definedCommands = {
            ('sayHello' + ' ' * (self._packageSize - len('sayHello'))) : self._sayHello
        }

        super().__init__()

    def listenCommand(self):
        # Receive commands
        cmd = self._socket.recv(self._packageSize).decode()

        self._definedCommands[cmd]()


    # Commands...
    def _sayHello(self):
        print('Naber Cinim??')

# Tests...
if __name__ == '__main__':
    # test command server-client
    cs = CommandServer()
    cc = CommandClient()

    time.sleep(2)

    cs.sendCommand(('sayHello' + ' ' * (constants['commandPackageSize'] - len('sayHello'))).encode())
