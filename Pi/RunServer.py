from ServerClient import *


vs = VideoServer()


for i in range(100):
    im = vs.receiveFrame()
    print('Writing ' + str(i+1) + '. image...')
    im.save('/tmp/RAM/cam' + str(i) + '.png')
    im.close()
