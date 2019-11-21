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

}

def getConstants():
    return constants
