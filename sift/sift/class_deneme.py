#! /usr/bin/env python3

import sys
import cv2
from sift import Siftir

try:
	arg1 = int(sys.argv[1])
except:
	arg1 = 5

try:
	arg2 = int(sys.argv[2])
except:
	arg2 = 4

images = ['2','7','8','10','23','26']

def read_and_crop_image(image_index):
	img = cv2.imread('../PoncikDataset/'+images[image_index]+'.jpg')
	with open('../PoncikDataset/'+images[image_index]+'.txt') as file:
		[x1,y1,x2,y2] = list(map(int,file.read().split(',')))
	h = y2-y1
	w = x2-x1
	return img[y1:y1+h+1,x1:x1+w+1]

def store_images(image_index):
	img = read_and_crop_image(image_index)
	filename = '../PoncikDataset/stored/'+images[image_index]+'.jpg'
	cv2.imwrite(filename,img)

my_sift = Siftir()

img = cv2.imread('../PoncikDataset/stored/'+images[arg1]+'.jpg')

losses = my_sift.check_image(img)

print(losses)
