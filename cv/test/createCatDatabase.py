'''
Create database by cropping the photos for the cats
'''

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

dirSources = input('Name of the directory containing images (multiple directories possible seperated by a space) : ')
dirDest   = input('Destination (empty for default ' + defaultOut + ') : ')

if dirDest == '':
    dirDest = defaultOut




for dirSource in dirSources.split():
    if not os.path.exists(dirDest + '/' + dirSource):
        print('Directory ' + dirDest + '/' + dirSource + ' does not exist, creating...')
        os.makedirs(dirDest + '/' + dirSource)

    filenames = os.listdir(dirSource)

    for filename in filenames:
        print('Processing ' + filename)
        im = cv2.imread(dirSource + '/' + filename)

        if im is None:
            print('Error ' + str(filename))
            continue

        classOut = classifier.classifyCatDog(im)

        if classOut['type'] == 'cat':
            if classOut['frame'].shape[1] < 50 or classOut['frame'].shape[0] < 50:
                print('Skipping filename ' + filename + 'Image size : ' + str(classOut['frame'].shape) + ' at ' + str(datetime.datetime.now()))
            else:
                print('Writing filename ' + filename)
                cv2.imwrite(dirDest + '/' + dirSource + '/' + filename, classOut['frame'])
        else:
            print('Cat not detected in ' + filename)
