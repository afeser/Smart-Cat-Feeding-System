import cv2
import numpy
import logging
from cv.src.Identifier import Identifier
import os
import sys

'''
Tester Siftir class

To start it, place it to the main directory by copying and start using python3
'''

work_dir = 'cv/data/SIFT'
logging.getLogger().setLevel(logging.INFO)

## Load sample images
im1 = cv2.imread(work_dir + '/resim.jpg')
doga1 = cv2.imread(work_dir + '/doga1_low.jpg')
doga2 = cv2.imread(work_dir + '/doga2_low.jpg')
doga3 = cv2.imread(work_dir + '/doga3_low.jpg')
doga4 = cv2.imread(work_dir + '/doga4_low.jpg')
doga5 = cv2.imread(work_dir + '/doga5_low.jpg')
utku1 = cv2.imread(work_dir + '/utku1_low.jpg')
utku2 = cv2.imread(work_dir + '/utku2_low.jpg')
utku3 = cv2.imread(work_dir + '/utku3_low.jpg')
utku4 = cv2.imread(work_dir + '/utku4_low.jpg')
utku5 = cv2.imread(work_dir + '/utku5_low.jpg')

doga1High = cv2.imread(work_dir + '/doga1.jpg')
doga2High = cv2.imread(work_dir + '/doga2.jpg')
doga1crop = cv2.imread(work_dir + '/doga1_crop.jpg')
doga2crop = cv2.imread(work_dir + '/doga2_crop.jpg')

## Class tests...
a = Identifier()
# a._databaseDir = 'cikti'

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
if not os.path.exists(work_dir + '/TEST'):
    os.makedirs(work_dir + '/TEST', exist_ok=True)
a.displaySIFT(doga1, work_dir + '/TEST/LowDogaOutput.jpg')
a.displaySIFT(doga1High, work_dir + '/TEST/HighDogaOutput.jpg')
a.displaySIFT(doga2High, work_dir + '/TEST/HighDogaOutput2.jpg')
a.displaySIFT(doga1crop, work_dir + '/TEST/Doga1Crop.jpg')
a.displaySIFT(doga2crop, work_dir + '/TEST/Doga2Crop.jpg')



b = Identifier()
b.resetDatabase(force=True)
b.importDirectory(work_dir + '/dataset')
sys.exit(0)

print(a.getCatName(doga5))
print(a.getCatName(utku5))
print(a.getCatName(im1))
