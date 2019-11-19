#!/usr/bin/python3
import pi.src.Server as Server
import pi.src.Constants as Constants
import cv.src.pythonYOLO as pythonYOLO


import cv2
import time
import numpy as np
import logging


'''
Server side controller. Brain and center of the whole project

Runs on a loop with a given time waits(frequency), or continously.
Decided to improve the design with version by adding new features in order to avoid confusion.

Design V1 :
Get image from pi with certain time intervals, classify it, send result to Pi
by activating Green or Red led.



TODO :
What if food is already given?

'''

logging.getLogger().setLevel(logging.INFO)

# Parameters...
waitBetweenFrames = 1 # in seconds


# Contruct server...
constants   = Constants.getConstants()

videoServer   = Server.VideoServer(constants)
commandServer = Server.CommandServer(constants)


while True:
    # V1 stuff...

    # Receive new frame
    frame = videoServer.receiveFrame()
    frame = np.array(frame)
    frame = frame[:, :, ::-1].copy()

    # Classify
    sinif = pythonYOLO.classifyCatDog(frame)


    # Send command
    if sinif == 'cat':
        logging.info('Cat detected')
        commandServer.greenLedOn()
    elif sinif == 'dog':
        logging.info('Dog detected')
        commandServer.redLedOn()
    elif sinif == 'NA':
        logging.info('Nothing detected')
        commandServer.allLedsOff()
    else:
        logging.warning('Unreasonable string from classifyCatDog')



    time.sleep(waitBetweenFrames)


# Below are some helper functions for scripting, not related to the Controller directly!
def saveImage(imName):
    pil_img     = videoServer.receiveFrame()
    numpy_image = np.array(pil_img)
    frame         = opencv_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(imName) + '.jpg', frame)
