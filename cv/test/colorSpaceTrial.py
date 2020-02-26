import numpy as np
import matplotlib.pyplot as plt
import cv2

histogramType = 'HSV'


plt.figure(figsize=(16,12)); plt.title('Ceren 1 ' + histogramType + ' Histogram'); plt.xlabel('Data Points'); plt.ylabel('Occurrences')
plt.hist(cv2.cvtColor(cv2.imread('ceren_1.jpg'), cv2.COLOR_BGR2HSV)[:,:,0].reshape(-1), bins=20, alpha=0.3)
plt.figure(figsize=(16,12)); plt.title('Ceren 2 ' + histogramType + ' Histogram'); plt.xlabel('Data Points'); plt.ylabel('Occurrences')
plt.hist(cv2.cvtColor(cv2.imread('ceren_2.jpg'), cv2.COLOR_BGR2HSV)[:,:,0].reshape(-1), bins=20, alpha=0.3)
plt.figure(figsize=(16,12)); plt.title('Esra 1 ' + histogramType + ' Histogram'); plt.xlabel('Data Points'); plt.ylabel('Occurrences')
plt.hist(cv2.cvtColor(cv2.imread('esra_1.jpg'), cv2.COLOR_BGR2HSV)[:,:,0].reshape(-1), bins=20, alpha=0.3)
plt.figure(figsize=(16,12)); plt.title('Esra 2 ' + histogramType + ' Histogram'); plt.xlabel('Data Points'); plt.ylabel('Occurrences')
plt.hist(cv2.cvtColor(cv2.imread('esra_2.jpg'), cv2.COLOR_BGR2HSV)[:,:,0].reshape(-1), bins=20, alpha=0.3)

plt.show()


