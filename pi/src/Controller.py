#!/usr/bin/python3
import Server
import Constants

'''
Server side

Currently under test...

'''

constants   = Constants.getConstants()

videoServer   = Server.VideoServer(constants)
# CommandClient = pi.src.Client.CommandClient()


# Below are some helper functions for scripting, not related to the Controller directly!
def saveImage(imName):
    pil_img     = videoServer.receiveFrame()
    numpy_image = np.array(pil_img)
    frame         = opencv_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(imName) + '.jpg', frame)
