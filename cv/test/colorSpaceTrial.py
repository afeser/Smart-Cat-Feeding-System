import numpy as np
import matplotlib.pyplot as plt
import cv2

histogramType = 'HSV'

bound=list(range(0,255,10))

images = []
images.append(['ceren_1.jpg', 'Ceren 1'])
images.append(['ceren_2.jpg', 'Ceren 2'])
images.append(['esra_1.jpg', 'Esra 1'])
images.append(['esra_2.jpg', 'Esra 2'])

names = {}
for image, name in images:
    plt.figure(figsize=(16,12)); plt.title(name + ' ' + histogramType + ' Histogram'); plt.xlabel('Data Points'); plt.ylabel('Occurrences')
    hist = plt.hist(cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2HSV)[:,:,0].reshape(-1), bins=bound, alpha=0.6)
    hist = hist[0] / np.sum(hist[0])

    names[name] = hist

# Error calculations...
#names = {'Ceren 1' : ceren1_hist, 'Ceren 2' : ceren2_hist, 'Esra 1' : esra1_hist, 'Esra 2' : esra2_hist}
for name1 in names:
    for name2 in names:
        if name1 == name2:
            continue

        print('Cost from {0:10s} to {1:10s} = {2:6f}'.format(name1, name2, np.sum(np.abs(names[name1] - names[name2]))))



plt.show()
