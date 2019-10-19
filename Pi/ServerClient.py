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
# import logging

constants = {
    # Some constants both for server and client
    "address"   : 'localhost',
    'videoPort' : 10004,
    'commandPort' : 10007,

    ### To be optimized...

    # _videoPackageSize : package size that stream read is done per receive request
    # To be optimized for performance. Used in stream server.
    'videoPackageSize' : 1024,
    # _commandPackageSize : package size that stream read is done per receive request
    # Not need to be optimized, already small data stream.
    'commandPackageSize' : 1024,

    # Frame per second, how many frames will the client send in sendFrame mode
    # Moreover, it can be dynamic in the future depending on the vision algorithm
    'fps' : 10

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


    def getAddress():
        return self._listenAddress

    def getPort():
        return self._listenPort



class VideoServer(Server):
    _serverName = 'VideoServer'

    def __init__(self):
        self._listenPort    = constants['videoPort']
        self._packageSize   = constants['videoPackageSize']


        Person.__init__(self)


    def receiveFrame(self, name):
        # Read a single image from the stream
        # TODO - images may stack! time may shift!

        data = clientsocket.recv(_packageSize)


class CommandServer(Server):
    _serverName = 'CommandServer'

    def __init__(self):
        self._listenPort    = constants['commandPort']
        self._packageSize   = constants['commandPackageSize']


        super().__init__()




    def _createServer(self, name):
        # Receive commands
        # Do different actions
        # Actions will be stored in a dictionary that belongs to the class

        # Accept connection - connection is already encrypted over SSH layer, so no check is required
        # it jumped to a new socket...
        (clientsocket, address) = self._serversocket.accept()

        self._clientsocket  = clientsocket
        self._clientaddress = address

        # Done! Main program will determine which command will be sent etc.

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
        self._desPort           = constants['videoPort']
        self._packageSize       = constants['videoPackageSize']
        self._fps               = constants['fps']
        self._frameSenderThread = None

        super()._init__()

    def startFrameSender(self):
        # Start frame sender thread
        # save the thread to kill later on request
        self._frameSenderThread = threading.Thread(target=self._startFrameSender, args=self, name='frameSender')
        self._frameSenderThread.start()

    def _startFrameSender(self):
        while True:
            # or wait for the transfer...
            time.sleep(1. / self._fps)

            # TODO - capture and send..
            .

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
