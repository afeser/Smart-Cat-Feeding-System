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
from cv.test.DatabaseCreator import DatabaseCreator
import pickle
import matplotlib.pyplot as plt
import matplotlib

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


def train_validation_test_accuracy(train_root_name, validation_root_name, test_root_name, new_cat_labels, databaseLocation=None, returns=[], optimize_database=False, save_name=''):
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

    save_name is used as prefix for the output files.

    '''

    a = Identifier(featureDescriptor='SIFT')




    # a.resetDatabase(force=True)
    if databaseLocation is None:
        a.importDirectory(train_root_name)


    # Not optimizing one possibilities
    elif os.path.exists(databaseLocation) and (not optimize_database):
        a.loadDatabase(databaseLocation=databaseLocation)
    elif (not os.path.exists(databaseLocation)) and (not optimize_database):
        a.importDirectory(train_root_name)
        a.saveDatabase(databaseLocation=databaseLocation)

    # Optimizing one possibilities
    elif os.path.exists(databaseLocation+'_optimized') and (optimize_database):
        a.loadDatabase(databaseLocation=databaseLocation+'_optimized')
    elif os.path.exists(databaseLocation) and optimize_database:
        a.loadDatabase(databaseLocation=databaseLocation)
        a.optimizeDatabase()
        a.saveDatabase(databaseLocation=databaseLocation+'_optimized')
    elif (not os.path.exists(databaseLocation)) and optimize_database:
        a.importDirectory(train_root_name)
        a.saveDatabase(databaseLocation=databaseLocation)
        a.optimizeDatabase()
        a.saveDatabase(databaseLocation=databaseLocation+'_optimized')



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
        confusion_matrix         = {diri2:{diri:0 for diri in all_classes_included} for diri2 in all_classes_included}
        time_spent               = {}
        totalClass               = {}
        totalCorrectClass        = {}
        for directory in directories:
            if directory in new_cat_labels:
                 current_class_name = 'None'
            else:
                 current_class_name = directory

            # confusion_matrix
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
        class_accuracy['NET'] = sum(map(lambda x : totalCorrectClass[x], totalCorrectClass)) / sum(map(lambda x : totalClass[x], totalClass))
        if 'print' in returns:
            print('Detailed accuracy report : ')

            for catName in totalClass:
                print('\t{0:30s} : {1:4f}'.format('Cat name ' + catName + ' with accuracy ', class_accuracy[catName]))

            print('Calculated accuracy is ' + str(class_accuracy['NET']))

        time_spent['NET'] = sum(time_spent.values()) / len(totalClass.values())

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
        workbook  = xlsxwriter.Workbook(save_name + 'confusion_matrix.xlsx')

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

    if 'accuracy' in returns:
        # Write to excel file...
        workbook  = xlsxwriter.Workbook(save_name + 'accuracy_results.xlsx')

        # Chart
        chart = workbook.add_chart({'type': 'column'})
        chart.set_x_axis({
            'name': 'Different Cat IDs',
            'name_font': {'size': 14, 'bold': True},
            'num_font':  {'italic': True },
            })
        chart.set_y_axis({
            'name': 'Accuracy Scores',
            'name_font': {'size': 14, 'bold': True},
            'num_font':  {'italic': True },
            })
        chart.set_title({'name' : 'Accuracy Results'})
        for set_name in ['train', 'validation', 'test']:
            all_cat_names = list(return_array[set_name]['accuracy'].keys())
            worksheet = workbook.add_worksheet(name=set_name)

            # First column
            worksheet.write(0, 0, 'Cat ID')
            for counter1, cat_name in enumerate(all_cat_names):
                worksheet.write(counter1+1, 0, cat_name)

            # Second column
            worksheet.write(0, 1, 'Accuracy')
            for counter1, cat_name in enumerate(all_cat_names):
                worksheet.write(counter1+1, 1, return_array[set_name]['accuracy'][cat_name])



            # Chart
            chart.add_series({'values': '=' + set_name + '!$A$2:$A$' + str(len(all_cat_names))})
            chart.add_series({'values': '=' + set_name + '!$B$2:$B$' + str(len(all_cat_names))})
        worksheet.insert_chart('D7', chart)

        workbook.close()

    if 'test_times' in returns:
        # Write to excel file...
        workbook  = xlsxwriter.Workbook(save_name + 'time_results.xlsx')

        # Chart
        chart = workbook.add_chart({'type': 'column'})
        chart.set_x_axis({
            'name': 'Different Cat IDs',
            'name_font': {'size': 14, 'bold': True},
            'num_font':  {'italic': True },
            })
        chart.set_y_axis({
            'name': 'Accuracy Scores',
            'name_font': {'size': 14, 'bold': True},
            'num_font':  {'italic': True },
            })
        chart.set_title({'name' : 'Accuracy Results'})
        for set_name in ['train', 'validation', 'test']:
            all_cat_names = list(return_array[set_name]['time_spent'].keys())
            worksheet = workbook.add_worksheet(name=set_name)

            # First column
            worksheet.write(0, 0, 'Cat ID')
            for counter1, cat_name in enumerate(all_cat_names):
                worksheet.write(counter1, 0, cat_name)

            # Second column
            worksheet.write(0, 1, 'Accuracy')
            for counter1, cat_name in enumerate(all_cat_names):
                worksheet.write(counter1, 1, str(return_array[set_name]['time_spent'][cat_name]))

            # Chart
            chart.add_series({'values': '=' + set_name + '!$A$2:$A$' + str(len(all_cat_names))})
            chart.add_series({'values': '=' + set_name + '!$B$2:$B$' + str(len(all_cat_names))})
        worksheet.insert_chart('D7', chart)

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
    test_sonuclari_hersey = []
    for counter in [6]:
        test_sonuclari = []
        for optimize in [False, True]:
            print('Test', counter, 'optimized = ' + str(optimize))


            dbCreator = DatabaseCreator()
            dbCreator.seperate_into_databases('Dataset_Cropped', join('metadata', 'dataset' + str(counter) + '.txt'), dest_dir='Dataset' + str(counter).zfill(2), override=True)

            train_root_name      = 'Dataset' + str(counter).zfill(2) + '/train'
            validation_root_name = 'Dataset' + str(counter).zfill(2) + '/validation'
            test_root_name       = 'Dataset' + str(counter).zfill(2) + '/test'
            with open(join('Dataset' + str(counter).zfill(2), 'excluded_classes.txt'), 'r') as class_file:
                new_cat_labels = class_file.readline().split()

                test_sonuclari.append(train_validation_test_accuracy(train_root_name, validation_root_name, test_root_name, new_cat_labels, 'utku_database'+str(counter), ['accuracy', 'confusion_matrix', 'print', 'test_times'], optimize_database=optimize, save_name='dataset'+str(counter)+'_optimize'+str(optimize)+'_'))


        # Extra plots...
        fig = plt.figure(figsize=(24, 18))
        font = {'family' : 'normal',
                'size'   : 28}

        matplotlib.rc('font', **font)


        # Accuracy plots...
        for set_name in ['train', 'validation', 'test']:
            plt.bar(list(test_sonuclari[0][set_name]['accuracy'].keys()), list(test_sonuclari[0][set_name]['accuracy'].values()))
            plt.bar(list(test_sonuclari[1][set_name]['accuracy'].keys()), list(test_sonuclari[1][set_name]['accuracy'].values()))
            plt.title('Optimized vs. Unoptimized for ' + set_name + 'set')
            plt.xlabel('Cat Identities')
            plt.ylabel('Accuracy Results')
            plt.legend(['Unoptimized', 'Optimized'])
            plt.xticks(rotation='vertical')

            plt.savefig('test' + str(counter) + set_name + '_set_accuracy_graph.png')

            plt.clf()

        # Speed plots...
        for set_name in ['train', 'validation', 'test']:
            plt.bar(list(test_sonuclari[0][set_name]['time_spent'].keys()), list(test_sonuclari[0][set_name]['time_spent'].values()))
            plt.bar(list(test_sonuclari[1][set_name]['time_spent'].keys()), list(test_sonuclari[1][set_name]['time_spent'].values()))
            plt.title('Optimized vs. Unoptimized for ' + set_name + 'set')
            plt.xlabel('Cat Identities')
            plt.ylabel('Time for Convergence(seconds)')
            plt.legend(['Unoptimized', 'Optimized'])
            plt.xticks(rotation='vertical')

            plt.savefig('test' + str(counter) + set_name + '_set_speed1_graph.png')

            plt.clf()

        plt.close(fig)

        test_sonuclari_hersey.append(test_sonuclari)

    pickle.dump(test_sonuclari_hersey, open('test_sonuclari_yedekleri.pickle', 'wb'))




test_utku()
