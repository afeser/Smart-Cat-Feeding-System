import cv2
import numpy
import logging
from cv.src.Classifier import Classifier
import os
import sys
import pdb
import datetime



classifier = Classifier(debug=False)

defaultOut = '/home/afeser/RAM/clippedImages'

dirSource = input('Name of the directory containing images (name_number.jpg) : ')
dirDest   = input('Destination (empty for default ' + defaultOut + ') : ')

if dirDest == '':
    dirDest = defaultOut

if not os.path.exists(dirDest):
    os.makedirs(dirDest)

files = os.listdir(dirSource)

for file in files:
    print('Processing ' + file)
    im = cv2.imread(dirSource + '/' + file)

    if im is None:
        print('Error ' + str(file))
        continue

    classOut = classifier.classifyCatDog(im)

    if classOut['type'] == 'cat':
        if classOut['frame'].shape[1] < 50 or classOut['frame'].shape[0] < 50:
            print('In file ' + file + ' image size : ' + str(classOut['frame'].shape) + ' at ' + str(datetime.datetime.now()))
        else:
            print('Writing file ' + file)
            cv2.imwrite(dirDest + '/' + file, classOut['frame'])
    else:
        print('Cat not detected in ' + file)
