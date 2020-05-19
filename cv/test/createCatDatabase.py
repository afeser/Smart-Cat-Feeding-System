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
from os.path import join
import enlighten



class DatabaseCreator:

    def __init__(self):
        self.classifier = Classifier(debug=False)

        self.defaultOut = '/home/afeser/RAM/clippedImages'

    def seperate_into_databases(self, source_database_dir, database_file_path, dest_dir='seperate_into_databases'):
        '''
        This part is going to seperate the original data into train, test and
        validation sets based on the file provided as input.


        This function expects the input database directory to be master. This
        means this directory should include directories that represent labels.
        SourceDirectory:
            01 -> label 01
            02 -> label 02
            03 -> label 03

        Output directory will be seperate_into_databases(can be change). The
        structure is:
            seperate_into_databases/01/image1.symlink
            seperate_into_databases/01/image2.symlink
            ...
            seperate_into_databases/02/image1.symlink
            seperate_into_databases/02/image1.symlink
            ...

        File format :
            10 # class sayisi bu -> kedi sayisi yani
            Train
            1
            20 # hangi resimlerin olacagi..
            Validation
            21
            30
            Test
            31
            40
        '''
        db_file  = open(database_file_path, 'r')

        lines = list(map(lambda x: x.split('#')[0], db_file.readlines()))

        num_classes = int(lines[0])

        train_start = int(lines[2])
        train_end   = int(lines[3])

        val_start   = int(lines[5])
        val_end     = int(lines[6])

        test_start  = int(lines[8])
        test_end    = int(lines[9])


        directories = os.listdir(source_database_dir)
        for directory in directories:
            if not os.path.exists(join(dest_dir, directory)):
                os.makedirs(join(dest_dir, directory))


            filenames = os.listdir(join(source_database_dir, directory))
            for filename in filenames:
                os.symlink(join(os.getcwd(), source_database_dir, directory, filename), join(dest_dir, directory, filename))






    def crop_rename(self, argv1=None, argv2=None):
        '''
        Can be used with arguments, or type input.

            >>> DatabaseCreator.crop_rename argv1=SourceDir argv2=DestDir -> no input, single source directory supported
            >>> DatabaseCreatorcrop_rename argv1=SourceDir               -> no input, single source directory supported
            >>> DatabaseCreatorcrop_rename                               -> asks input


        Crop and rename images if they are not renamed.

        If the data source directory does not contain any files, it is assumed to be a
        master folder that contains directories which are assumed to be labels. If more
        than one directory is given, skips the master part.

        More examples:
            >>> DatabaseCreator.crop_rename()
            Name of the directory containing images (multiple directories possible seperated by a space) : 01 02
            Destination (empty for default ... ) :
            --------> this will process photos inside folders 01 and 02

            >>> DatabaseCreator.crop_rename()
            Name of the directory containing images (multiple directories possible seperated by a space) : MASTER
            Destination (empty for default ... ) :
            --------> this will process photos inside folders MASTER/01 MASTER/02 MASTER/03 ...

            >>> DatabaseCreator.crop_rename(argv1='02')
            --------> this will process photos inside folder 02

            >>> DatabaseCreator.crop_rename(argv1='MASTER')
            --------> this will process photos inside folders MASTER/01 MASTER/02 MASTER/03 ...

            >>> DatabaseCreator.crop_rename(argv1='01', argv2='dest')
            --------> this will process photos inside folder 01 and puts the output at dest folder

        '''
        if argv1 is None:
            dirSources = input('Name of the directory containing images (multiple directories possible seperated by a space) : ').split()
            dirDest   = input('Destination (empty for default ' + self.defaultOut + ') : ')

            if dirDest == '':
                dirDest = self.defaultOut

        else:
            dirSources = [argv1]
            if argv2 is None:
                dirDest = self.defaultOut
            else:
                dirDest = argv2


        # Check if this is a master directory for the complete dataset...
        if len(dirSources) == 1:
            dirSource = dirSources[0]
            names = os.listdir(dirSource)

            logging.info('Processing files in the given directory')
            for name in names:
                if os.path.isfile(join(dirSource, name)):
                    break
            else:
                logging.info('Master directory detected. Descending the sub-directories')
                dirSources = list(map(lambda x: join(dirSource, x), names))


        bar = enlighten.Counter(total=sum(list(map(len, list(map(os.listdir, dirSources))))))
        for dirSource in dirSources:
            if not os.path.exists(join(dirDest, dirSource)):
                logging.info('Directory ' + dirDest + '/' + dirSource + ' does not exist, creating...')
                os.makedirs(join(dirDest, dirSource))

            filenames = os.listdir(dirSource)

            # All files in that class...
            nameCounter = 0
            for filename in filenames:
                logging.info('Processing ' + filename)
                im = cv2.imread(dirSource + '/' + filename)

                if im is None:
                    logging.warning('File ' + str(filename) + ' can not be opened!')
                    continue

                classOut = self.classifier.classifyCatDog(im)

                if classOut['type'] == 'cat':
                    if classOut['frame'].shape[1] < 50 or classOut['frame'].shape[0] < 50:
                        logging.info('Skipping filename ' + dirSource + '/' + filename + 'Image size : ' + str(classOut['frame'].shape) + ' at ' + str(datetime.datetime.now()))
                    else:
                        hedef = join(dirDest, dirSource, str(nameCounter) + '.jpg')
                        logging.info('Writing filename ' + str(hedef))
                        cv2.imwrite(hedef, classOut['frame'])
                        nameCounter = nameCounter + 1
                else:
                    logging.info('Cat not detected in ' + filename)

                bar.update()




dbc = DatabaseCreator()
# DatabaseCreator().crop_rename('Original')
dbc.seperate_into_databases('Original', 'db1_metadata.txt', dest_dir='Dataset1')
dbc.seperate_into_databases('Original', 'db2_metadata.txt', dest_dir='Dataset2')
dbc.seperate_into_databases('Original', 'db2_metadata.txt', dest_dir='Dataset3')
