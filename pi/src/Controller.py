#!/usr/bin/python3
import pi.src.Server as Server
import pi.src.Constants as Constants
from cv.src.Classifier import Classifier


import cv2
import time
import numpy as np
import logging
import sys
from PIL import Image

'''
Server side controller. Brain and center of the whole project

Runs on a loop with a given time waits(frequency), or continously.
Decided to improve the design with version by adding new features in order to avoid confusion.

Design V1 :
Get image from pi with certain time intervals, classify it, send result to Pi
by activating Green or Red led as well as opening and closing the food gate.



TODO :
What if food is already given?

'''

debugMode = False
if len(sys.argv) > 1 and sys.argv[1] == 'debug':
    debugMode = True

    logging.basicConfig(level=logging.DEBUG)

# Parameters...
waitBetweenFrames = 1 # in seconds


# Contruct server...
constants   = Constants.getConstants()


videoServer   = Server.VideoServer(constants)
commandServer = Server.CommandServer(constants)

neuralNetwork = Classifier(debugMode=debugMode)

# TODO - bunu dogru yere tasimaliyiz...


while True:
    # V1 stuff...

    # Receive new frame
    frame = videoServer.receiveFrame()
    if debugMode:
        frame.save('receivedBufferImage.png')


    frame = np.array(frame)

    # Discaring alpha channel...
    frame = frame[:,:,:3]
    frame = frame[:, :, ::-1].copy()
    if debugMode:
        # Write image
        logging.info('Received image shape ' + str(frame.shape))
        logging.info('Writing received image as receivedImage.jpg...')
        cv2.imwrite('receivedImage.jpg', frame)

    # TODO - return of picture can be moved to the Server
    frame = cv2.flip(frame, 0) # reversed camera...
    if debugMode:
        logging.info('Flipped image shape ' + str(frame.shape))
        logging.info('Writing flipped image as flippedImage.jpg...')
        cv2.imwrite('flippedImage.jpg', frame)

    # Classify
    sinif = neuralNetwork.classifyCatDog(frame)


    # Send command
    commandServer.allLedsOff()
    if sinif == 'cat':
        logging.info('Cat detected')
        commandServer.greenLedOn()
        commandServer.feedCat()
    elif sinif == 'dog':
        logging.info('Dog detected')
        commandServer.redLedOn()
    elif sinif == 'NA':
        logging.info('Nothing detected')
        commandServer.yellowLedOn()
    else:
        logging.warning('Unreasonable string from classifyCatDog')



    time.sleep(waitBetweenFrames)


# Below are some helper functions for scripting, not related to the Controller directly!
def saveImage(imName):
    pil_img     = videoServer.receiveFrame()
    numpy_image = np.array(pil_img)
    frame         = opencv_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(imName) + '.jpg', frame)
