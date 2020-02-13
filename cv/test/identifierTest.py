import cv2
import numpy
import logging
from cv.src.Identifier import Identifier
import os
import sys
import pdb

'''
Tester Siftir class

To start it, place it to the main directory by copying and start using python3
'''

work_dir = 'cv/data/SIFT'
logging.getLogger().setLevel(logging.DEBUG)

def test1():
    # Old test for saveCat, not used anymore...


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
    a.saveSIFTImage(doga1, work_dir + '/TEST/LowDogaOutput.jpg')
    a.saveSIFTImage(doga1High, work_dir + '/TEST/HighDogaOutput.jpg')
    a.saveSIFTImage(doga2High, work_dir + '/TEST/HighDogaOutput2.jpg')
    a.saveSIFTImage(doga1crop, work_dir + '/TEST/Doga1Crop.jpg')
    a.saveSIFTImage(doga2crop, work_dir + '/TEST/Doga2Crop.jpg')



    b = Identifier()
    b.resetDatabase(force=True)
    b.importDirectory(work_dir + '/dataset')
    sys.exit(0)

    print(a.getCatName(doga5))
    print(a.getCatName(utku5))
    print(a.getCatName(im1))

def test2():

    root_name = work_dir + '/FacebookDataset13/'
    a = Identifier(featureDescriptor='ORB')



    print('Importing directory...')
    a.importDirectory(work_dir + '/FacebookDataset13')
    a.resetDatabase(force=True)
    a.saveDatabase()

    # pdb.set_trace()
    files = os.listdir(root_name)
    print('Plotting recognized vectors over images')
    for file in files:
        basename  = file.split('_')[0]
        im = cv2.imread(root_name + file)
        a.saveSIFTImage(im, dest=work_dir + '/FacebookDataset13SIFTOutput/' + file, sourceDesc=a._database[basename])

    # Accuracy calculation
    total   = 0
    correct = 0
    for file in files:
        basename = file.split('_')[0]
        im = cv2.imread(root_name + file)

        predictedClass = a.getCatName(im)

        print('Cat name is ' + basename + ' and predicted name is ' + predictedClass)

        total = total + 1
        if basename == predictedClass:
            correct = correct + 1

    print('Calculated accuracy is ' + str(correct / total))
    return a

a = test2()
