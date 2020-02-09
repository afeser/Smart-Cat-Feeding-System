import cv.src.siftir
import cv2
import numpy
import logging

'''
Tester Siftir class
'''

logging.getLogger().setLevel(logging.INFO)

## Load sample images
im1 = cv2.imread('resim.jpg')
doga1 = cv2.imread('doga1_low.jpg')
doga2 = cv2.imread('doga2_low.jpg')
doga3 = cv2.imread('doga3_low.jpg')
doga4 = cv2.imread('doga4_low.jpg')
doga5 = cv2.imread('doga5_low.jpg')
utku1 = cv2.imread('utku1_low.jpg')
utku2 = cv2.imread('utku2_low.jpg')
utku3 = cv2.imread('utku3_low.jpg')
utku4 = cv2.imread('utku4_low.jpg')
utku5 = cv2.imread('utku5_low.jpg')

## Class tests...
a = sift.Siftir()
a._databaseDir = 'cikti'

a.saveCat(doga1, 'doga')
a.saveCat(doga2, 'doga')
a.saveCat(doga3, 'doga')
a.saveCat(doga4, 'doga')
a.saveCat(utku1, 'utku')
a.saveCat(utku2, 'utku')
a.saveCat(utku3, 'utku')
a.saveCat(utku4, 'utku')
# a.saveCat(im1, 'rainbow')


## Visual investigation
a.displaySIFT(doga1)

print(a.getCatName(doga5))
print(a.getCatName(utku5))
print(a.getCatName(im1))
