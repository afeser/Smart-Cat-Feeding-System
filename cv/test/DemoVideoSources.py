import numpy as np
import cv2
import pdb
import os
import matplotlib.pyplot as plt
import copy
import enlighten

prefix = './'

def draw_rectangle_animation(img, rectangle_start, rectangle_end, color='g'):
    '''
    Give input name and corrdinates.


    '''
    print('Classifying the object...')
    bar = enlighten.Counter(total= 2*(sum(rectangle_end) - sum(rectangle_start)))

    if color == 'r':
        color = (0, 0, 255)
    elif color == 'g':
        color = (0, 255, 0)

    line_width = 3


    counter_file = 0
    # edge 1, upper horizontal
    for counter in range(rectangle_start[0], rectangle_end[0]):
        cv2.imwrite('output/' + prefix + str(counter_file).zfill(4) + 'square_animation.jpg', img)
        for line_counter in range(line_width):
          img[rectangle_start[1]-line_counter, counter, :] = color
        counter_file = counter_file + 1
        bar.update()

    # edge 1, right vertical
    for counter in range(rectangle_start[1], rectangle_end[1]):
        cv2.imwrite('output/' + prefix + str(counter_file).zfill(4) + 'square_animation.jpg', img)
        for line_counter in range(line_width):
          img[counter, rectangle_end[0]+line_counter, :] = color
        counter_file = counter_file + 1
        bar.update()


    # edge 1, lower horizontal
    target_array = list(range(rectangle_start[0], rectangle_end[0]))
    target_array.reverse()
    for counter in target_array:
        cv2.imwrite('output/' + prefix + str(counter_file).zfill(4) + 'square_animation.jpg', img)
        for line_counter in range(line_width):
          img[rectangle_end[1]+line_counter, counter, :] = color
        counter_file = counter_file + 1
        bar.update()

    # edge 1, left vertical
    target_array = list(range(rectangle_start[1], rectangle_end[1]))
    target_array.reverse()
    for counter in target_array:
        cv2.imwrite('output/' + prefix + str(counter_file).zfill(4) + 'square_animation.jpg', img)
        for line_counter in range(line_width):
          img[counter, rectangle_start[0]-line_counter, :] = color
        counter_file = counter_file + 1
        bar.update()








class ORB:
    def image_detect_and_compute(detector, img):
        """Detect and compute interest points and their descriptors."""

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        kp = detector.detect(img, None)
        kp, des = detector.compute(img, kp)
        return img, kp, des


    def draw_image_matches(detector, img1_name, img2_name, nmatches=10):
        '''
        Draw ORB feature matches of the given two images.
        '''
        img1, kp1, des1 = ORB.image_detect_and_compute(detector, img1_name)
        img2, kp2, des2 = ORB.image_detect_and_compute(detector, img2_name)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key = lambda x: x.distance) # Sort matches by distance.  Best come first.

        img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:nmatches], img2, flags=2) # Show top 10 matches
        plt.figure(figsize=(32, 32))
        plt.title(type(detector))
        plt.imshow(img_matches); plt.show()
    def create_vectors_one_at_a_time(im1):
        '''
        Give image as input. This will write results to xxxx_sift_vectors.jpg
        '''
        sift = cv2.xfeatures2d.SIFT_create()
        img1_renkli = copy.copy(im1)

        img1, kp1, des1 = ORB.image_detect_and_compute(sift, im1)

        draw_params = dict(matchColor=(0, 255, 0), singlePointColor=(255, 0, 0), flags=0)


        print('Processing key points...')
        bar = enlighten.Counter(total=len(kp1))
        keypoint_resmi = img1_renkli.copy()
        for indexx in range(len(kp1)):
            keypoint_resmi = cv2.drawMatchesKnn(keypoint_resmi, [kp1[indexx]], np.array([[[0,0,0]]]), [], [], None, **draw_params)
            keypoint_resmi = keypoint_resmi[:img1.shape[0], :img1.shape[1], :]
            cv2.imwrite('output/' + str(indexx).zfill(4) + 'sift_vectors.jpg', keypoint_resmi)
            bar.update()

    def animate_draw_matches(im1, im2):
        '''
        Give image as input, it will process the new vectors and match them with the second image.
        '''
        line_width = 3


        sift = cv2.xfeatures2d.SIFT_create()
        img1_renkli = copy.copy(im1)
        img2_renkli = copy.copy(im2)

        img1, kp1, des1 = ORB.image_detect_and_compute(sift, im1)
        img2, kp2, des2 = ORB.image_detect_and_compute(sift, im2)


        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params,search_params)
        matches = flann.knnMatch(des1, des2, k=3)
        matches = [[x[0], x[-1]] for x in matches]

        draw_params = dict(matchColor=(0, 255, 0), singlePointColor=(255, 0, 0), flags=0)

        match_index = []
        for i, (m, n) in enumerate(matches):
            if m.distance < 0.55*n.distance:
                match_index.append(i)

        print('Processing key points...')
        # UZUNLUK HESAPLAMAK ICIN
        toplam_uzunluk = 0
        for match_counter in range(len(match_index)):
            # nedense image 1 ile kp1 yerleri farkli, kanser etti beni yav...
            point1 = kp1[matches[match_index[match_counter]][0].queryIdx].pt # (x_kordonati, y_kordinati) seklinde bu, numpy array ise tersi
            point1 = (point1[1], point1[0]) # numpy array sekline getir..
            # keypoint_resmi[int(point1[1]):int(point1[1]+2), int(point1[0]):int(point1[0]+2), :] = (0, 0, 255)
            point2 = kp2[matches[match_index[match_counter]][0].trainIdx].pt
            point2 = (point2[1], point2[0] + im2.shape[1])

            toplam_uzunluk = toplam_uzunluk + int(point2[1] - point1[1])

        bar = enlighten.Counter(total=len(kp1) + len(kp2) + toplam_uzunluk)
        # Ilk resim yuklemesi
        keypoints_processed_1 = []
        image_counter = 0
        for indexx in range(len(kp1)):
            keypoints_processed_1.append(kp1[indexx])
            keypoint_resmi = cv2.drawMatchesKnn(img1_renkli, keypoints_processed_1, img2_renkli, [], [], None, **draw_params)
            cv2.imwrite('output/' + str(image_counter).zfill(5) + 'sift_vectors_mathces.jpg', keypoint_resmi)
            bar.update()
            image_counter = image_counter + 1

        keypoints_processed_2 = []
        for indexx in range(len(kp2)):
            keypoints_processed_2.append(kp2[indexx])
            keypoint_resmi = cv2.drawMatchesKnn(img1_renkli, keypoints_processed_1, img2_renkli, keypoints_processed_2, [], None, **draw_params)
            cv2.imwrite('output/' + str(image_counter).zfill(5) + 'sift_vectors_mathces.jpg', keypoint_resmi)
            bar.update()
            image_counter = image_counter + 1

        # print('matching start' + str(image_counter))
        for match_counter in range(len(match_index)):
            # nedense image 1 ile kp1 yerleri farkli, kanser etti beni yav...
            point1 = kp1[matches[match_index[match_counter]][0].queryIdx].pt # (x_kordonati, y_kordinati) seklinde bu, numpy array ise tersi
            point1 = (point1[1], point1[0]) # numpy array sekline getir..
            # keypoint_resmi[int(point1[1]):int(point1[1]+2), int(point1[0]):int(point1[0]+2), :] = (0, 0, 255)
            point2 = kp2[matches[match_index[match_counter]][0].trainIdx].pt
            point2 = (point2[1], point2[0] + im2.shape[1])


            # test...
            # keypoint_resmi[int(point2[0]):int(point2[0]+5), int(point2[1]):int(point2[1]+5), :] = (0, 0, 255)
            # keypoint_resmi[int(point1[0]):int(point1[0]+5), int(point1[1]):int(point1[1]+5), :] = (0, 0, 255)

            # pdb.set_trace()
            # artik tum data (y, x) seklinde..

            color = (0, 255, 0)
            egim  = (point2[0] - point1[0]) / (point2[1] - point1[1])
            for x_sayici in range(int(point2[1] - point1[1])):
                for line_width_counter in range(line_width):
                    keypoint_resmi[int(point1[0]+x_sayici*egim)+line_width_counter, int(point1[1]+x_sayici)+line_width_counter, :] = color

                bar.update()
                cv2.imwrite('output/' + str(image_counter).zfill(5) + 'sift_vectors_mathces.jpg', keypoint_resmi)
                image_counter = image_counter + 1







# cem1 = cv2.imread('resim.jpg')
# print()
# draw_rectangle_animation(cem1, [77, 70], [464, 482])
# print()
# print('Cat detected with confidence 0.97')
# draw_rectangle_animation(cem1, [77, 70], [464, 482])
# print('Dog detected!')
#
#
# cem1 = cv2.imread('resim.jpg')[70:482, 77:464, :]
# ORB.create_vectors_one_at_a_time(cem1)
# print('New cat detected and registered to database!')

cem1 = cv2.imread('cem_1.jpg')[70:482, 77:464, :]
cem2 = cv2.imread('cem_2.jpg')[121:483, 100:486, :]
ORB.animate_draw_matches(cem2, cem1)
print('Cat recognized as already registered!')

# kopek = cv2.imread('kopek.jpg')
# draw_rectangle_animation(kopek, [57,45], [447,602], color='r')
# print()
# print('Dog detected with confidence 1.00')

# Video icin...
# ffmpeg -r 5 -start_number 0 -i %04dsift_vectors.jpg  -pix_fmt yuv420p out.mp4 # -r 5 -> 5 picture frame per second...
# -q:v  2 -> mallamamasini sagliyor -> https://video.stackexchange.com/questions/8621/ffmpeg-output-is-blocky
