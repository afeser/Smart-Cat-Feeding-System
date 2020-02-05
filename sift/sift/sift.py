import cv2
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
from glob import glob
import numpy as np
import pickle

class Siftir:
	def __init__(self):
		self._sift = cv2.xfeatures2d.SIFT_create(contrastThreshold=0.05, edgeThreshold=10, sigma = 1.8)
		self._stored_images = glob('../PoncikDataset/stored/*.jpg')

	def _display_feature_vectors(self,img,kp):
		""" Displays the feature vectors of an image. """
		keypoints = cv2.drawKeypoints(img,kp,img)
		winname = 'iyi'
		cv2.namedWindow(winname)
		cv2.moveWindow(winname, 0, 0)
		cv2.imshow(winname, keypoints)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def _get_descriptors(self,img):
		""" Returns the feature vectors of an image. """

		kp, desc = self._sift.detectAndCompute(img, None)
		if desc is None:
			return  np.random.randint(190, size=(1, 128))
		# self._display_feature_vectors(img,kp)
		return desc

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
