# Server-Client code for data and command stream
# Test script for Server and Client

# Source(s) :
# https://docs.python.org/2/howto/sockets.html
# https://stackoverflow.com/questions/21233340/sending-string-via-socket-python


# Definitions :
# 1) Sometimes it is confusing that which side is server. Usually streaming side
# is assumed to be the server. However, in this configuration to clearly define
# the virtual machine server, server always refer to virtual machine.
#    Server : virtual machine server
#    Client : raspberry pi zero


# TODO(s)
# 1) Error-Handling
# 2) Logging
# 3) Connection lost-reconnection


from Server import *
from Client import *


import sys
import os

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


if sys.argv[1] == 'test1C':
    cc = CommandClient(constants)

    print(cc._receiveStr())

if sys.argv[1] == 'test1S':
    string = sys.argv[2]
    cs = CommandServer(constants)

    cs._sendStr(string)


if sys.argv[1] == 'test2S':
    vs = VideoServer(constants)

    dirName = sys.argv[2]

    for i in range(2):
        im = vs.receiveFrame(returnBytesIO=True)
        # print('Writing ' + str(i+1) + '. image...')
        with open (dirName + '/' + str(i) + '.png', 'wb') as f:
            f.write(im.getvalue())


if sys.argv[1] == 'test2C':
    vc = VideoClient(constants)

    dirName = sys.argv[2]

    for i in range(2):
        vc.listener([dirName + '/' + str(i) + '.png'])
