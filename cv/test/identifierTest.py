import cv2
import numpy
import logging
from cv.src.Identifier import Identifier
import os
import sys
import pdb
from os.path import join
import multiprocessing
from cv.test.MetadataParser import MetadataParser
import enlighten
import xlsxwriter
import time

'''
Tester Siftir class

To start it, place it to the main directory by copying and start using python3
'''

logging.basicConfig(filename='identifier_test_log.txt', level=logging.NOTSET)

def train_validation_test_accuracy(train_root_name, validation_root_name, test_root_name, metadata_file_path, databaseLocation=None, returns=[]):
    parser = MetadataParser()
    parser.parse(metadata_file_path)

    excludes = parser.get_value('all_exludes')

    train_validation_test_accuracy(train_root_name, validation_root_name, test_root_name, excludes, databaseLocation, returns)


def train_validation_test_accuracy(train_root_name, validation_root_name, test_root_name, new_cat_labels, databaseLocation=None, returns=[]):
    '''
    Give train data root directory and test data root directory.
    Directory structure :
    train_root_name/class_1/image1.jpg

    test_root_name/class_1/image2.jpg

    New cat labels are given so that they are not classified as false.
    Example :
        ['label_08', 'label_09']

    Set databaseLocation if you want to save that database; otherwise, database will be trashed after tests are done.


    returns variable is for the desired return values of the system. Return variable
    will be a list of variables with the same order as returns variable.
    Example :
        ['accuracy']
        ['print'] -> print accuracy values
        ['confusion_matrix'] -> save confusion_matrix to excel file named as confusion_matrix.xlsx
        ['confusion_matrix', 'test_times']
        [...]



    '''

    a = Identifier(featureDescriptor='SIFT')




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

        print(test_name + ' set computations...')
        bar = enlighten.Counter(total=sum(map(lambda direc : len(os.listdir(join(target_dir, direc))), directories)))


        all_classes_included = list(set(['None'] + directories) - set(new_cat_labels))
        confusion_matrix         = {}
        confusion_matrix['None'] = {diri:0 for diri in all_classes_included}
        time_spent               = {}
        totalClass               = {}
        totalCorrectClass        = {}
        for directory in directories:
            if directory in new_cat_labels:
                 current_class_name = 'None'
            else:
                 current_class_name = directory

            # confusion_matrix
            confusion_matrix[current_class_name]  = {diri:0 for diri in all_classes_included}
            totalClass[current_class_name]        = 0
            totalCorrectClass[current_class_name] = 0
            time_spent[current_class_name]        = 0

            filenames = os.listdir(join(target_dir, directory))
            for filename in filenames:
                bar.update()
                im = cv2.imread(join(target_dir, directory, filename))

                time_start     = time.time()
                predictedClass = a.getCatId(im)
                time_end       = time.time()

                time_spent[current_class_name] = time_spent[current_class_name] + (time_end - time_start)

                # confusion_matrix
                confusion_matrix[current_class_name][predictedClass] = confusion_matrix[current_class_name][predictedClass] + 1

                totalClass[current_class_name] = totalClass[current_class_name] + 1
                if current_class_name == predictedClass:
                    totalCorrectClass[current_class_name] = totalCorrectClass[current_class_name] + 1


            time_spent[current_class_name] = time_spent[current_class_name] / totalClass[current_class_name]

        class_accuracy                 = {catName:totalCorrectClass[catName] / totalClass[catName] for catName in totalClass}
        class_accuracy['net_accuracy'] = sum(map(lambda x : totalCorrectClass[x], totalCorrectClass)) / sum(map(lambda x : totalClass[x], totalClass))
        if 'print' in returns:
            print('Detailed accuracy report : ')

            for catName in totalClass:
                print('\t{0:30s} : {1:4f}'.format('Cat name ' + catName + ' with accuracy ', class_accuracy[catName]))

            print('Calculated accuracy is ' + str(class_accuracy['net_accuracy']))

        time_spent['all_average'] = sum(time_spent.values()) / sum(totalClass.values())

        return_array = {}
        for return_request in returns:
            if return_request == 'test_times':
                return_array['time_spent'] = time_spent
            elif return_request == 'accuracy':
                return_array['accuracy'] = class_accuracy
            elif return_request == 'confusion_matrix':
                return_array['confusion_matrix'] = confusion_matrix
            elif return_request == 'print':
                pass
            else:
                raise ValueError('Given value is not recognized ' + str(return_request))

        return return_array




    return_array = {}
    return_array['train']      = calc_accuracy(train_root_name, 'train')
    return_array['validation'] = calc_accuracy(validation_root_name, 'validation')
    return_array['test']       = calc_accuracy(test_root_name, 'test')

    if 'confusion_matrix' in returns:
        # Write to excel file...
        workbook  = xlsxwriter.Workbook('confusion_matrix.xlsx')

        for set_name in ['train', 'validation', 'test']:
            all_cat_names = list(return_array[set_name]['confusion_matrix'].values())[0].keys()
            worksheet = workbook.add_worksheet(name=set_name)

            # First column
            for counter1, cat_name in enumerate(all_cat_names):
                worksheet.write(counter1+1, 0, cat_name)

            # First row
            for counter1, cat_name in enumerate(all_cat_names):
                worksheet.write(0, counter1+1, cat_name)

            # Matrix...
            for counter1, from_cat_name in enumerate(all_cat_names):
                for counter2, to_cat_name in enumerate(all_cat_names):
                    worksheet.write(counter1+1, counter2+1, return_array[set_name]['confusion_matrix'][from_cat_name][to_cat_name])

        workbook.close()

    return return_array

def train_validation_test_bench():
    '''
    18 May 2020 Utku Serhan Database Test V1
    '''
    train_root_name      = 'train'
    validation_root_name = 'val'
    test_root_name       = 'test'
    new_cat_labels       = ['07', '08']
    train_validation_test_accuracy(train_root_name, validation_root_name, test_root_name, new_cat_labels, 'database_utku_V1')



def test_utku():
    counter = 2
    train_root_name      = 'Dataset' + str(counter).zfill(2) + '/train'
    validation_root_name = 'Dataset' + str(counter).zfill(2) + '/validation'
    test_root_name       = 'Dataset' + str(counter).zfill(2) + '/test'
    with open(join('Dataset' + str(counter).zfill(2), 'excluded_classes.txt'), 'r') as class_file:
        new_cat_labels = class_file.readline().split()

        train_validation_test_accuracy(train_root_name, validation_root_name, test_root_name, new_cat_labels, 'utku_database2_optimized', ['accuracy', 'confusion_matrix', 'print', 'test_times'])


test_utku()
