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

logging.basicConfig(filename='identifier_test_log.txt', level=logging.NOTSET)

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

def train_validation_test_bench():
    '''
    18 May 2020 Utku Serhan Database Test V1
    '''
    train_root_name      = 'train'
    validation_root_name = 'val'
    test_root_name       = 'test'
    new_cat_labels       = ['07', '08']
    train_validation_test_accuracy(train_root_name, validation_root_name, test_root_name, new_cat_labels, 'database_utku_V1')


for counter in range(1, 10):
    train_root_name      = 'Dataset' + str(counter).zfill(2) + '/train'
    validation_root_name = 'Dataset' + str(counter).zfill(2) + '/validation'
    test_root_name       = 'Dataset' + str(counter).zfill(2) + '/test'
    with open(join('Dataset' + str(counter).zfill(2), 'excluded_classes.txt'), 'r') as class_file:
        new_cat_labels = class_file.readline().split()

    train_validation_test_accuracy(train_root_name, validation_root_name, test_root_name, new_cat_labels, 'utku_database' + str(counter))
