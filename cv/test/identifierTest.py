import cv2
import numpy
import logging
from cv.src.Identifier import Identifier
import os
import sys
import pdb
from os.path import join

'''
Tester Siftir class

To start it, place it to the main directory by copying and start using python3
'''

work_dir = 'cv/data/SIFT'
logging.basicConfig(filename='identifier_test_log.txt', level=logging.DEBUG)

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
    # a.saveSIFTImage(doga1, work_dir + '/TEST/LowDogaOutput.jpg')
    # a.saveSIFTImage(doga1High, work_dir + '/TEST/HighDogaOutput.jpg')
    # a.saveSIFTImage(doga2High, work_dir + '/TEST/HighDogaOutput2.jpg')
    # a.saveSIFTImage(doga1crop, work_dir + '/TEST/Doga1Crop.jpg')
    # a.saveSIFTImage(doga2crop, work_dir + '/TEST/Doga2Crop.jpg')



    b = Identifier()
    # b.resetDatabase(force=True)
    b.importDirectory(work_dir + '/dataset')
    sys.exit(0)

    print(a.getCatId(doga5))
    print(a.getCatId(utku5))
    print(a.getCatId(im1))

def train_validation_test_accuracy(train_root_name, validation_root_name, test_root_name, new_cat_labels, databaseLocation=None):
    '''
    Give train data root directory and test data root directory.
    Directory structure :
    train_root_name/class_1/image1.jpg

    test_root_name/class_1/image2.jpg

    New cat labels are given so that they are not classified as false.
    Example :
        ['label_08', 'label_09']

    Set databaseLocation if you want to save that database; otherwise, database will be trashed after tests are done.
    '''

    a = Identifier(featureDescriptor='SIFT', debug=True)




    # a.resetDatabase(force=True)
    if databaseLocation is None:
        # No database, import and do not save
        a.importDirectory(train_root_name)
    elif os.path.exists(databaseLocation):
        # Use existing database as it exists
        a.loadDatabase(databaseLocation=databaseLocation)
    else:
        a.importDirectory(train_root_name)
        a.saveDatabase(databaseLocation=databaseLocation)


    def calc_accuracy(target_dir, test_name):
        '''
        Calculate accuracy based on files under given directory.

        Directory is train / test / validation set directory.
        Example :
            27MarchTrainSet

        Test name is only for print purposes.
        Example :
            train
            test



        Example Use :
            calc_accuracy('dataset/train_images', 'train')
            calc_accuracy('dataset/test_images', 'test')
        '''

        directories = os.listdir(target_dir)

        total   = 0
        correct = 0
        print(test_name + ' set accuracy computations...')
        totalClass        = {}
        totalCorrectClass = {}
        for directory in directories:
            totalClass[directory]        = 0
            totalCorrectClass[directory] = 0

            filenames = os.listdir(join(target_dir, directory))
            for filename in filenames:
                im = cv2.imread(join(target_dir, directory, filename))

                predictedClass = a.getCatId(im)

                print('Actual {0:20} -> predicted {1:20}'.format(directory, predictedClass))

                total = total + 1
                totalClass[directory] = totalClass[directory] + 1
                if directory == predictedClass:
                    totalCorrectClass[directory] = totalCorrectClass[directory] + 1
                    correct = correct + 1

                if directory in new_cat_labels and predictedClass == 'None':
                    totalCorrectClass[directory] = totalCorrectClass[directory] + 1
                    correct = correct + 1


        print('Detailed accuracy report : ')

        for catName in totalClass:
            print('\t{0:30s} : {1:4f}'.format('Cat name ' + catName + ' with accuracy ', totalCorrectClass[catName] / totalClass[catName]))

        print('Calculated accuracy is ' + str(correct / total))


    # calc_accuracy(train_root_name, 'train')
    calc_accuracy(validation_root_name, 'validation')
    calc_accuracy(test_root_name, 'test')

    return a

def test2():
    '''
    18 May 2020 Utku Serhan Database Test V1
    '''
    train_root_name      = 'train'
    validation_root_name = 'val'
    test_root_name       = 'test'
    new_cat_labels       = ['07', '08']
    train_validation_test_accuracy(train_root_name, validation_root_name, test_root_name, new_cat_labels, 'database_utku_V1')

test2()
