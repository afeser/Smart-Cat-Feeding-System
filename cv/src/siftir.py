import cv2
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
from glob import glob
import numpy as np
import pickle
import os
import logging
import datetime

class Siftir:
	'''
	This class contains scalability problems. Storage, processing power, computation
	time is designed for very few data such as 100-200 different cats. Generalizing to
	more data makes this class obsolete, new improvements would be requred.
	'''

	def __init__(self):
		# self._sift = cv2.xfeatures2d.SIFT_create(contrastThreshold=0.05, edgeThreshold=10, sigma = 1.8)
		self._sift = cv2.xfeatures2d.SIFT_create(edgeThreshold=2, contrastThreshold=0.05)

		'''
		Database directory
			- cat name(unqiue id)
				- vector stack 1
				- vector stack 2
				- ...

		Each vector stack contains a list of vectors
		'''
		self._databaseDir = 'cv/data/SIFT/database'


		if not os.path.exists(self._databaseDir):
			os.makedirs(self._databaseDir, exist_ok=True)


		self._savedCats = os.listdir(self._databaseDir)


	def _getSavedSiftVectors(self, id):
		'''
		Get saved sift vectors from given id.

		Return list of vectors matching the cat
		'''
		vectors = []
		dirName = self._databaseDir + '/' + id + '/'
		for filename in os.listdir(dirName):
			with open(dirName + filename, 'rb') as f:
				vectors.extend(pickle.load(f))

		return vectors

	def _getSiftVectors(self, im):
		'''
		Return vectors for the given image
		'''
		kp, desc = self._sift.detectAndCompute(im, None)
		if desc is None:
			return  np.random.randint(190, size=(1, 128))
		# self._display_feature_vectors(img,kp)
		return desc

	def displaySIFT(self,img):
		""" Displays the feature vectors of an image. """
		kp, desc = self._sift.detectAndCompute(img, None)

		# keypoints = cv2.drawKeypoints(img,kp,img)
		# winname = 'Feature Vectors'
		# cv2.namedWindow(winname)
		# cv2.moveWindow(winname, 0, 0)
		# TODO - cross
		cv2.imwrite('SiftImage,jog', keypoints)


	def check_image(self, img1):
		""" Compares img1 with the stored images.

		All feature vectors in img1 is compared with all stored image vectors.
		Stored images will be referred as img2. Each vector of img1 stores its
		eulidean distance to the closest vector in img2. The minimum distances
		for all img1 vectors are summed up together to decide an overall loss
		between the two images. This comparison is then done for each img2. The
		returned dictionary stores the loss values.

		Parameters
		----------
		img1 : cv2.image
			The input image that needs to be compared to the stored images

		Returns
		-------
		dict
			{
			string: float,
			...
			string: float
			}

			Where each string stands for a stored image and each float is its error with respect to img1

		"""
		descriptors1 = self._get_descriptors(img1)
		losses = {}
		for img_name in self._stored_images:
			img = cv2.imread(img_name)
			descriptors2 = self._get_descriptors(img)
			losses[img_name[24:]] = 0
			for descriptor1 in descriptors1:
				min = -1
				for descriptor2 in descriptors2:
					distance = np.linalg.norm(descriptor1-descriptor2)
					if distance < min or min < 0:
						min = distance
					if min == 0:
						break
				losses[img_name[24:]] += min
		return losses


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
		for cat in self._savedCats:
			# Each vector
			savedVectors = np.array(self._getSavedSiftVectors(cat))
			for savedVector in savedVectors:
				for currentVector in currentVectors:
					dist = np.linalg.norm(currentVectors - savedVector)
					if nearests[1][9] > dist:
						ekle(nearests, dist, cat)


		endTime = (datetime.datetime.now() - startTime).total_seconds()
		logging.info('Identified in ' + str(endTime) + ' seconds')

		# TODO - birkac taneye bakilmali!
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
		vectors = self._getSiftVectors(catImage)
		logging.info('Saving ' + str(len(vectors)) + ' SIFT vectors for ' + uniqueId)

		if not os.path.exists(self._databaseDir + '/' + uniqueId):
			os.makedirs(self._databaseDir + '/' + uniqueId, exist_ok=True)

		with open(self._databaseDir + '/' + uniqueId + '/' + datetime.datetime.now().strftime('%d-%b-%Y_%H-%M-%S') + '.pickle', 'wb') as f:
			pickle.dump(vectors, f)

		if not uniqueId in self._savedCats:
			self._savedCats.append(uniqueId)

	def importDirectory(self, directoryPath):
		'''
		Import every file in a directory based on their base names

		poncik.jpg -> imported with unique id 'poncik'

		Parameters
		----------
		directoryPath : string, path of the directory for images

		Returns
		-------
		None
		'''
		pass

	def resetDatabase(self):
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
		if input('Are you sure want to delete whole database? (y/N)') == 'y':
			pass
