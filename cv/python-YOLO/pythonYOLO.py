import cv2

# Source :
# https://www.youtube.com/watch?v=xKK2mkJ-pHU
# https://www.pyimagesearch.com/2017/11/06/deep-learning-opencvs-blobfromimage-works/


# Load YOLO
net = cv2.dnn.readNet("YOLO/yolov3-tiny.weights", "YOLO/yolov3.cfg")

# Preprocessing
