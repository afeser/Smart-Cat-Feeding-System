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
            logging.info('No database file found, creating an empty one')
            self._database = {}
        else:
            logging.info('Found a database file, loading...')
            self.loadDatabase()


        self._vectorThreshold = 60


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

    def saveSIFTImage(self, img, dest='SiftImage.jpg', sourceDesc=None):
        '''
        Create SIFT image and save it to the file.

        Parameters
        ----------
        desc : a list of descriptors to highlight, only show this descriptors if they exist
        '''
        kp, desc_source = self._getSiftVectors(img, returnKP=True)

        desc = []
        keypoints = cv2.drawKeypoints(img,kp,img)
        if not sourceDesc is None:
            for des in desc_source:
                for sourceDes in sourceDesc:
                    if self.equal(sourceDes, des):
                        desc.append(des)

        else:
            desc = desc_source

        # winname = 'Feature Vectors'
        # cv2.namedWindow(winname)
        # cv2.moveWindow(winname, 0, 0)
        # TODO - cross
        logging.info('Writing to file ' + dest)

        # for keypoint in kp:
            # pdb.set_trace()
            # point = (int(keypoint.pt[0]), int(keypoint.pt[1]))
            # cv2.circle(img, point, 1, (0,180,0))
        cv2.imwrite(dest, img)



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


        # 2)
        for catName in localImages:
            logging.info('Processing ' + str(catName) + ' to import from directory')
            vectors = self._createSiftVectors(localImages[catName])

            print('Total vectors adding to database for class ' + str(catName) + ' is ' + str(len(vectors)))

            if catName not in self._database:
                self._database[catName] = []

            # 3)
            self._database[catName].extend(vectors)

    def equal(self, vector1, vector2):
        return np.linalg.norm(vector1 - vector2) < self._vectorThreshold

    def _createSiftVectors(self, images):
        '''
        This is the method to extract sift vectors based on the common ones among
        pictures. Note that, every time a new picture is added, whole database
        should be updated. Note this is very computationally expensive and
        future versions may need to improve the algorithm.


        Algorithm :
        - Find common features in images by
            for each image1 in images:
                for each image2 in images except image1:
                    if a feature matches, include it in the sift vectors for this class
        '''


        completeVectors = []
        for index1, image1 in enumerate(images):
            logging.debug('Creating SIFT vectors for image ' + str(index1) + ' and all of the remaining images for that class.')
            for index2, image2 in enumerate(images):

                # pdb.set_trace()
                if index1 != index2:
                    siftVectors1 = self._getSiftVectors(image1)
                    siftVectors2 = self._getSiftVectors(image2)

                    # Brute force match all of the vectors
                    for index3, vector1 in enumerate(siftVectors1):
                        # logging.debug('Vector ' + str(index3) + ' is being processed')
                        for vector2 in siftVectors2:
                            if self.equal(vector1, vector2):
                                completeVectors.append(vector1)

        # Eliminate duplicates
        for index1, vector1 in enumerate(completeVectors):
            for index2, vector2 in enumerate(completeVectors):
                if index1 != index2 and np.array_equal(vector1, vector2):
                    completeVectors.pop(index1)

        return completeVectors


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
            logging.warning('Resetting feature database...')
            os.remove(self._databaseDir + '/siftVectors.pickle')
        else:
            # Nothing made
            pass
