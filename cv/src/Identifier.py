import cv2
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
from glob import glob
import numpy as np
import pickle
import os
import logging
import datetime
import pdb
import matplotlib.pyplot as plt
import datetime
import time

class Identifier:
    '''
    This class contains scalability problems. Storage, processing power, computation
    time is designed for very few data such as 100-200 different cats. Generalizing to
    more data makes this class obsolete, new improvements would be requred.

    Dictionary is used as a database. Each cat name has the corresponding SIFT vectors.
    These are dumped into pickle file.
    '''

    def __init__(self, featureDescriptor='SIFT'):
        if featureDescriptor == 'SIFT':
            self._featureDescriptor = cv2.xfeatures2d.SIFT_create()
        elif featureDescriptor == 'ORB':
            # TODO - also set matchers!!!
            # pdb.set_trace()
            self._featureDescriptor = cv2.ORB_create()

        else:
            raise NameError('Feature descriptor ' + str(featureDescriptor) + ' is not defined!')

        # self._featureDescriptor = cv2.xfeatures2d.SIFT_create(contrastThreshold=0.15, edgeThreshold=10, sigma = 1.8)

        '''
        Database directory
            - cat name(unqiue id)
                - vector stack 1
                - vector stack 2
                - ...

        Each vector stack contains a list of vectors
        '''
        self._databaseDir = 'cv/data/SIFT/database'

        # Create new database if does not exist
        if not os.path.exists(self._databaseDir):
            logging.info('No database directory found, creating an empty one')
            os.makedirs(self._databaseDir, exist_ok=True)
            self._database = {}


        if not os.path.exists(self._databaseDir + '/siftVectors.pickle'):
            logging.warning('No database file found, creating an empty one')
            self._database = {}
        else:
            logging.warning('Found a database file, loading...')
            self.loadDatabase()


        # Descriptor and matching parameters other than the object itself
        self._ratioTestThreshold = 0.55


        # Performance measurement
        self._timeStart = time.time()

    def loadDatabase(self):
        '''
        Load the whole database.

        Data is a simple dictionary object.
        '''
        dirName = self._databaseDir + '/siftVectors.pickle'
        with open(dirName, 'rb') as f:
            self._database = pickle.load(f)



    def saveDatabase(self):
        '''
        Save the whole database.

        Data is a simple dictionary object.
        '''
        logging.info('Overwriting the existing database')

        dirName = self._databaseDir + '/siftVectors.pickle'
        with open(dirName, 'wb') as f:
            pickle.dump(self._database, f)



    def _getSiftVectors(self, im, returnKP=False):
        '''
        Return vectors for the given image
        '''
        kp, desc = self._featureDescriptor.detectAndCompute(im, None)
        if desc is None:
            # TODO - dense sift olacak burada...
            desc =  []
            kp   =  []
        # self._display_feature_vectors(img,kp)

        if returnKP:
            return (kp, desc)
        else:
            return desc




    def getCatName(self, catImage):
        '''
        See check_image for detailed calculation.

        Get an image and return the most relevant name of it. Find the cat unique id.


        Parameters
        ----------
        catImage : cv2.image
            The input image that needs to be compared to the stored images

        Returns
        -------
        string
        '''

        '''
        Algorithm

        1) Compare all vectors
        2) For the best match 10 !! Hyperparameter, identify it
        '''
        startTime = datetime.datetime.now()
        def ekle(nearests, distance, id):
            '''
            Find the point to insert, and insert it...
            '''
            for i in range(len(nearests[0])):
                if nearests[1][i] > distance:
                    nearests[1].insert(i, distance)
                    nearests[0].insert(i, id)
                    nearests[1].pop()
                    nearests[0].pop()



        currentVectors = np.array(self._getSiftVectors(catImage))

        # TODO - dynamic yapilcak
        # Ids, distance
        # [smallest distance, ..., greatest distance]
        nearests = ([-1]*10, [10000]*10)
        for catName in self._database:

            # Each vector
            for catVector in self._database[catName]:
                for currentVector in currentVectors:
                    dist = np.linalg.norm(currentVectors - catVector)
                    if nearests[1][9] > dist:
                        ekle(nearests, dist, catName)


        endTime = (datetime.datetime.now() - startTime).total_seconds()
        logging.info('Identified in ' + str(endTime) + ' seconds')

        # TODO - birkac taneye bakilmali!
        if nearests[0][0] == -1:
            return 'nothing'
        else:
            return nearests[0][0]


    def saveCat(self, catImage, uniqueId):
        '''
        Extract SIFT vectors and save to database with uniqueId.

        Parameters
        ----------
        catImage : cv2.image
            The input image whose vectors will be stored
        uniqueId : A string, which uniquely defines the cat image given

        Returns
        -------
        None
        '''
        # TODO...

    def debugTime(self, customStr='', reset=False):
        if reset:
            # Reset time without writing anything
            self._timeStart = time.time()
            return

        if customStr != '':
            logging.debug('Time elapsed for ' + customStr + ' ' + str(- self._timeStart + time.time()) + ' seconds')
        else:
            logging.debug('Time elapsed ' + ' ' + str(- self._timeStart + time.time()) + ' seconds')

        self._timeStart = time.time()


    def importDirectory(self, directoryPath):
        '''
        TODO - it only works for empty database

        Import every file in a directory based on their base names

        poncik_1.jpg -> imported with unique id 'poncik'

        Parameters
        ----------
        directoryPath : string, path of the directory for images

        Returns
        -------
        None

        Algorithm :
        1) Read each image
        2) When finished, send them to the sift creator
        3) Compile all of them into database
        '''
        files = os.listdir(directoryPath)

        localImages = {

        }
        # 1)
        for file in files:
            logging.debug('Reading file ' + file)
            basename  = file.split('_')[0]

            targetFile = self._databaseDir + '/' + basename + '/' + basename + '.pickle'


            if basename not in localImages:
                localImages[basename] = []

            im = cv2.imread(directoryPath + '/' + file)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            localImages[basename].append(im)


        def _createSiftVectorsFromImageSet(images, catName):
            '''
            This is the method to extract sift vectors based on the common ones among
            pictures. Note that, every time a new picture is added, whole database
            should be updated. Note this is very computationally expensive and
            future versions may need to improve the algorithm.


            Algorithm :
            - Find common features in images by brute force approach (BFMatcher) or FLANN based approach
            - Add them for each combination!

            A better algorithm may be found, feel free to add and change it. However,
            common ones are the only useful thing I imagined.
            '''
            # Debug mode
            if logging.getLogger().level <= 10:
                debugDir = self._databaseDir + '/debug'
                logging.debug('Debug mode on, saving match results into ' + debugDir)
                os.makedirs(debugDir, exist_ok=True)
                flann = cv2.FlannBasedMatcher({'algorithm' : 0, 'trees' : 5})

                completeVectors = []
                for index1, image1 in enumerate(images):
                    for index2, image2 in enumerate(images):

                        if index1 != index2:
                            keypoints1, siftVectors1 = self._getSiftVectors(image1, returnKP=True)
                            keypoints2, siftVectors2 = self._getSiftVectors(image2, returnKP=True)

                            logging.debug('Matching key points with flann matcher')
                            matches = flann.knnMatch(siftVectors1, siftVectors2, k=2)
                            self.debugTime('flann match')
                            # Save the matches
                            matchesMask = [[0, 0] for i in range(len(matches))]
                            # ratio test as per Lowe's paper
                            logging.debug('Finding the correct key points according to Lowe\'s paper')
                            self.debugTime(reset=True)
                            for i, match in enumerate(matches):
                                if match[0].distance < match[1].distance*self._ratioTestThreshold:
                                    # Add it!
                                    completeVectors.append(siftVectors1[match[0].queryIdx])
                                    completeVectors.append(siftVectors2[match[0].trainIdx])

                                    matchesMask[i] = [0, 1]
                            self.debugTime('find keys')


                            draw_params = dict(matchColor=(0, 255, 0),
                                            singlePointColor=(255, 0, 0),
                                            matchesMask=matchesMask,
                                            flags=0)

                            img3 = cv2.drawMatchesKnn(image1, keypoints1, image2, keypoints2, matches, None, **draw_params)
                            new_fig = plt.figure(figsize=(32, 32))
                            plt.imshow(img3)
                            plt.savefig(debugDir + '/' + catName + '_' + str(index1) + '_' + str(index2) + '.png')
                            plt.close(new_fig)



                # Eliminate duplicates
                for index1, vector1 in enumerate(completeVectors):
                    for index2, vector2 in enumerate(completeVectors):
                        if index1 != index2 and np.array_equal(vector1, vector2):
                            completeVectors.pop(index1)

                return completeVectors

            flann = cv2.FlannBasedMatcher({'algorithm' : 0, 'trees' : 5})

            completeVectors = []
            for index1, image1 in enumerate(images):
                for index2, image2 in enumerate(images):

                    if index1 != index2:
                        siftVectors1 = self._getSiftVectors(image1)
                        siftVectors2 = self._getSiftVectors(image2)

                        # pdb.set_trace()
                        matches = flann.knnMatch(siftVectors1, siftVectors2, k=2)

                        for match in matches:
                            if match[0].distance < match[1].distance*self._ratioTestThreshold:
                                # Add it!
                                completeVectors.append(siftVectors1[match[0].queryIdx])
                                completeVectors.append(siftVectors2[match[0].trainIdx])


            # Eliminate duplicates
            for index1, vector1 in enumerate(completeVectors):
                for index2, vector2 in enumerate(completeVectors):
                    if index1 != index2 and np.array_equal(vector1, vector2):
                        completeVectors.pop(index1)

            return completeVectors

        # 2)
        for catName in localImages:
            logging.info('Processing ' + str(catName) + ' to import from directory')


            vectors = _createSiftVectorsFromImageSet(localImages[catName], catName)

            logging.info('Total vectors adding to database for class ' + str(catName) + ' is ' + str(len(vectors)))

            if catName not in self._database:
                self._database[catName] = []

            # 3)
            self._database[catName].extend(vectors)


    def resetDatabase(self, force=False):
        '''
        Remove everything from database, delete any imported, saved data.
        Be careful when using!

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        if force or input('Are you sure want to delete whole database? (y/N)') == 'y':
            try:
                logging.warning('Resetting feature database...')
                os.remove(self._databaseDir + '/siftVectors.pickle')
            except FileNotFoundError:
                logging.warning('No feature database found, skipping...')

        else:
            # Nothing made
            pass
