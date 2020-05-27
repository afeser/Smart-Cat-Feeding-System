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
import sys
import enlighten
from multiprocessing import Pool


class Identifier:
    '''
    This class contains scalability problems. Storage, processing power, computation
    time is designed for very few data such as 100-200 different cats. Generalizing to
    more data makes this class obsolete, new improvements would be requred.

    Dictionary is used as a database. Each cat name has the corresponding SIFT vectors.
    These are dumped into pickle file.
    '''


    # Initialization...
    def __init__(self, featureDescriptor='SIFT', debug=False):
        if featureDescriptor == 'SIFT':
            self._featureDescriptor = cv2.xfeatures2d.SIFT_create()
        elif featureDescriptor == 'ORB':
            # TODO - also set matchers!!!
            # pdb.set_trace()
            self._featureDescriptor = cv2.ORB_create()
        else:
            raise NameError('Feature descriptor ' + str(featureDescriptor) + ' is not defined!')

        # Database stuff
        self._databaseDir = 'database'
        self._database    = {}
        if not os.path.exists(self._databaseDir):
            # logging.info('No database directory found, creating an empty one')
            os.makedirs(self._databaseDir)

        # Descriptor and matching
        self._ratioTestThreshold = 0.35
        self._flann = cv2.FlannBasedMatcher({'algorithm' : 0, 'trees' : 5})
        self._new_cat_threshold = 100
        self._new_cat_distances = []

        # Performance measurement
        self._timeStart = time.time()
        self._debug = debug

    # Database stuff...
    def loadDatabase(self, databaseLocation=None):
        '''
        Load the whole database.

        Data is a simple dictionary object.
        '''
        if databaseLocation is None:
            dirName = self._databaseDir + '/siftVectors.pickle'
        else:
            dirName = databaseLocation

        with open(dirName, 'rb') as f:
            [self._database, self._new_cat_threshold] = pickle.load(f)
    def saveDatabase(self, databaseLocation=None):
        '''
        Save the whole database.

        Data is a simple dictionary object.
        '''
        logging.info('Overwriting the existing database')

        if databaseLocation is None:
            dirName = self._databaseDir + '/siftVectors.pickle'
        else:
            dirName = databaseLocation

        with open(dirName, 'wb') as f:
            pickle.dump([self._database, self._new_cat_threshold], f)
    def importDirectory(self, directoryPath):
        '''
        Import every file in a directory based on their class directories

        class_01/{img1.jpg, img2.jpg, ...}
        class_02/{img1.jpg, img2.jpg, ...}

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
        # A directory represents a class
        directories = os.listdir(directoryPath)
        directories.sort()


        localImages = {

        }
        # 1)
        for directory in directories:
            filenames = os.listdir(os.path.join(directoryPath, directory))
            localImages[directory] = []

            for filename in filenames:
                logging.debug('Reading file ' + filename)

                im = cv2.imread(os.path.join(directoryPath, directory, filename))

                im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                localImages[directory].append(im)


        def _createSiftVectorsFromImageSet(images, catId, bar):
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
            if self._debug:
                debugDir = self._databaseDir + '/debug'
                logging.debug('Debug mode on, saving match results into ' + debugDir)
                os.makedirs(debugDir, exist_ok=True)

                completeVectors = []
                for index1, image1 in enumerate(images):
                    for index2, image2 in enumerate(images):
                        bar.update()
                        # pdb.set_trace()

                        if index1 != index2:
                            keypoints1, siftVectors1 = self._getSiftVectors(image1, returnKP=True)
                            keypoints2, siftVectors2 = self._getSiftVectors(image2, returnKP=True)

                            logging.debug('Matching key points with flann matcher')
                            matches = self._flann.knnMatch(siftVectors1, siftVectors2, k=2)
                            self._debugTime('flann match')
                            # Save the matches
                            matchesMask = [[0, 0] for i in range(len(matches))]
                            # ratio test as per Lowe's paper
                            logging.debug('Finding the correct key points according to Lowe\'s paper')
                            self._debugTime(reset=True)
                            for i, match in enumerate(matches):
                                if match[0].distance < match[1].distance*self._ratioTestThreshold:
                                    # Add it!
                                    completeVectors.append(siftVectors1[match[0].queryIdx])
                                    completeVectors.append(siftVectors2[match[0].trainIdx])

                                    matchesMask[i] = [0, 1]

                                    self._new_cat_distances.append(match[0].distance)

                            self._debugTime('find keys')


                            draw_params = dict(matchColor=(0, 255, 0),
                                            singlePointColor=(255, 0, 0),
                                            matchesMask=matchesMask,
                                            flags=0)

                            img3 = cv2.drawMatchesKnn(image1, keypoints1, image2, keypoints2, matches, None, **draw_params)
                            new_fig = plt.figure(figsize=(32, 32))
                            plt.imshow(img3)
                            plt.savefig(debugDir + '/' + catId + '_' + str(index1+1) + '_' + str(index2+1) + '.png')
                            plt.close(new_fig)



                self._new_cat_threshold = sum(self._new_cat_distances) / len(self._new_cat_distances)

                return completeVectors

            else:
                completeVectors = []
                for index1, image1 in enumerate(images):
                    for index2, image2 in enumerate(images):
                        bar.update()

                        if index1 != index2:
                            siftVectors1 = self._getSiftVectors(image1)
                            siftVectors2 = self._getSiftVectors(image2)

                            # pdb.set_trace()
                            matches = self._flann.knnMatch(siftVectors1, siftVectors2, k=2)

                            for match in matches:
                                if match[0].distance < match[1].distance*self._ratioTestThreshold:
                                    # Add it!
                                    completeVectors.append(siftVectors1[match[0].queryIdx])
                                    completeVectors.append(siftVectors2[match[0].trainIdx])


                return completeVectors

        # 2)
        print('Creating database')
        bar = enlighten.Counter(total=sum(map(lambda x: len(x)**2, localImages.values())))
        for catId in localImages:
            logging.info('Processing ' + str(catId) + ' to import from directory')


            vectors = _createSiftVectorsFromImageSet(localImages[catId], catId, bar)

            logging.info('Total vectors adding to database for class ' + str(catId) + ' is ' + str(len(vectors)))

            if catId not in self._database:
                self._database[catId] = []

            # 3)
            self._database[catId].extend(vectors)
    def optimizeDatabase(self):
        '''
        Optimizing database by;
            - eliminating duplicate vectors # TODO -> equal'in tanimini duzgun yapmaliyiz!
            - eliminating vectors that are very similar but in `different class of images`!

        '''
        def eliminateDuplicateVectors(database):
            '''
            Since it requires a lot of time, importing directory does not call
            eliminate duplicate vectors from database.
            It can be done by manually calling this function.

            It eliminates for every class...
            '''



            all_processes = []
            allCatIds = list(database.keys())

            print('Printing approximate progress..')
            bar = enlighten.Counter(total=len(self._database[allCatIds[-1]]))

            p = Pool(4)
            # print(list(map(lambda catId : (database, catId, self._new_cat_threshold), allCatIds[:-1])))
            # a,b,c=list(map(lambda catId: [self, catId, bar], allCatIds))[0]
            # print(b)
            # pdb.set_trace()
            eliminateList = p.map_async(Identifier._eliminateDuplicateVectors_parallel, list(map(lambda catId: [self._database[catId], self._new_cat_threshold], allCatIds[:-1])));


            catId = allCatIds[-1]
            eliminateThose = []

            for index1, vector1 in enumerate(database[catId]):
                bar.update()
                for index2, vector2 in enumerate(database[catId]):

                    if index1 != index2 and np.linalg.norm(vector1 - vector2) < self._new_cat_threshold: # TODO : note this is static!
                        eliminateThose.append(index1)

            eliminateThose = list(np.unique(eliminateThose))
            eliminateThose.sort(reverse=True)


            p.close()
            p.join()
            eliminateList.append(eliminateThose)
            for counter, identity in enumerate(liminateThose):
                for el in identity:
                    database[allCatIds[counter]].pop(el)





        def eliminateVectorsInDifferentClasses():
            '''
                An idea!
                    Find the matching vectors in the same class of images and
                    find the common vectors among two different classes of images.
                    Then eliminate the ones with greater threshold.
            '''
            pass

        # Invoke functions...
        eliminateDuplicateVectors(self._database)
        eliminateVectorsInDifferentClasses()
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
    def databaseInfo(self):
        '''
        Print database information
        '''
        print('Number of classes in total : ' + str(len(self._database)))

        print('{0:30s}'.format('Number of vectors per class : '))
        total = 0
        for className in self._database:
            print('\t{0:30s} : {1:5d}'.format(className, len(self._database[className])))
            total = total + len(self._database[className])

        print('\t' + '_' * 30 + ' : ' + '_' * 4 + '+')
        print('\t{0:30s} : {1:5d}'.format('Total', total))

    # Private definitions...
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
    def _debugTime(self, customStr='', reset=False):
        if reset:
            # Reset time without writing anything
            self._timeStart = time.time()
            return

        if customStr != '':
            logging.debug('Time elapsed for ' + customStr + ' ' + str(- self._timeStart + time.time()) + ' seconds')
        else:
            logging.debug('Time elapsed ' + ' ' + str(- self._timeStart + time.time()) + ' seconds')

        self._timeStart = time.time()
    def _eliminateDuplicateVectors_parallel(argsss):
        database, new_cat_threshold = argsss

        eliminateThose = []
        for index1, vector1 in enumerate(database):
            for index2, vector2 in enumerate(database):

                if index1 != index2 and np.linalg.norm(vector1 - vector2) < new_cat_threshold: # TODO : note this is static!
                    eliminateThose.append(index1)
                pass

        eliminateThose = list(np.unique(eliminateThose))
        eliminateThose.sort(reverse=True)

        return eliminateThose

    # Most commonly used in public...
    def getCatId(self, catImage):
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

        for each iamge class :
            Compare with FLANN

        Find the maximum number of matches...
        '''
        self._debugTime(reset=True)

        k = 5 # another hyperparameter, look below...


        startTime = time.time()
        catDesc = self._getSiftVectors(catImage)

        matchNumber    = {}
        allDescriptors = []
        boundaries     = [0]
        # TODO -> bu precompute edilebilir...
        for catId in self._database:
            boundaries.append(boundaries[-1] + len(self._database[catId]))
            allDescriptors.extend(self._database[catId])
        boundaries = np.array(boundaries)

        matches = self._flann.match(catDesc, np.array(allDescriptors))

        # find the smallest k distances, these distances give the correct class
        smallestIndices   = [-1] * k
        smallestDistances = [100000] * k
        for match in matches:
            if smallestDistances[k-1] > match.distance:
                k_temp = k - 1
                while k_temp >= 1 and smallestDistances[k_temp-1] > match.distance:
                    smallestDistances[k_temp] = smallestDistances[k_temp-1]
                    smallestIndices[k_temp]   = smallestIndices[k_temp-1]
                    k_temp = k_temp - 1

                smallestDistances[k_temp] = match.distance
                smallestIndices[k_temp]   = match.trainIdx

                # Correctness test, check if sorted...
                # if not all(smallestDistances[i] <= smallestDistances[i+1] for i in range(len(smallestDistances)-1)):
                #     print('FAILED!')
                #     sys.exit(1)

                # print(smallestDistances)

        # Map indices to cat names...
        catIds = list(self._database)

        for k_temp in range(k):
            # pdb.set_trace()
            # print(smallestIndices[k_temp] > boundaries)
            smallestIndices[k_temp] = catIds[np.sum(smallestIndices[k_temp] > boundaries)-1]

        # logging.info('Identified with ' + str(maxMatchNumber) + ' vectors as ' + maxMatchName + ' in ' + str(time.time() - startTime) + ' seconds')
        mostFrequent = {}
        for label in smallestIndices:
            if label in mostFrequent:
                mostFrequent[label] = mostFrequent[label] + 1
            else:
                mostFrequent[label] = 0 # or 1, does not matter

        maxLabel = list(mostFrequent)[0]
        maxVal   = mostFrequent[maxLabel]
        for key in mostFrequent:
            if mostFrequent[key] > maxVal:
                maxLabel = key
                maxVal   = mostFrequent[key]

        self._debugTime('flann match')
        # pdb.set_trace()
        if smallestDistances[0] < self._new_cat_threshold: # static threshold for new cat, currently working !
            return maxLabel # str(list(mostFrequent))
        else:
             return 'None'
    def addNewCat(self, catId, catVectors):
        '''
        When a cat seen firstly, add it to the database.

        - Take at least 2 shots, find the matching vectors,
            - Find the maximum distance between these vectors, based on this distance
                remove the ones that exists on other images smaller than this threshold.
        '''
        pass
