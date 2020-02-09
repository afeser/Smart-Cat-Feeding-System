import cv2
import numpy as np
import time
import logging

class Classifier:

    def __init__(self, debugMode=False):

        logging.info('Loading YOLO weights and configuration...')

        self._net = cv2.dnn.readNet('cv/data/YOLO/yolov3.weights', "cv/data/YOLO/yolov3.cfg")
        self._classes = []

        logging.info('Loading Coco names and forming classes...')

        with open('cv/data/YOLO/coco.names', 'r') as f:
            self._classes = [line.strip() for line in f.readlines()]
        layer_names = self._net.getLayerNames()
        self._output_layers = [layer_names[i[0] - 1] for i in self._net.getUnconnectedOutLayers()]


        self._debugMode = debugMode

    def classifyCatDog(self, frame):
        '''
        TODO
        1) Return of object coordinates are wrong!
        '''
        startTime = time.time()
        debug     = self._debugMode
        classes   = self._classes

        logging.info('Detecting objects (forming blobs)..')
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)

        self._net.setInput(blob)

        logging.info('Forwarding through layers...')
        # Find objects for each channel
        outs = self._net.forward(self._output_layers)

        # Surpression and calculating parameters

        logging.info('Forming frame shape and determining rectangle coordinates...')
        height, width, channels = frame.shape

        class_ids = []
        confidences = []
        boxes = []
        self._rect = None
        for out in outs:
            # 80 classes - 5 extra
            for detection in out:
                # detection -> probabilities of outputs of 80
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:

                    self._rect = {}

                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    self._rect['w'] = int(detection[2] * width)
                    self._rect['h'] = int(detection[3] * height)

                    # Rectangle coordinates
                    self._rect['x'] = int(center_x - self._rect['w'] / 2)
                    self._rect['y'] = int(center_y - self._rect['h'] / 2)

                    boxes.append([self._rect['x'], self._rect['y'], self._rect['w'], self._rect['h']])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        logging.info('Surpressing boxes detected for same objects...')
        # TODO - buna bakacagiz
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)


        detectedClasses = [self._classes[id] for id in class_ids]


        def debugFunc():
            font = cv2.FONT_HERSHEY_PLAIN
            colors = np.random.uniform(0, 255, size=(len(classes), 3))

            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = confidences[i]
                    color = colors[class_ids[i]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, color, 3)



            logging.info('Writing the image to the folder...')
            t = time.localtime()
            timestamp = time.strftime('%b-%d-%Y_%H%M%S', t)
            cv2.imwrite("frame_" + timestamp + ".jpg", frame)



        logging.info('Calling nested debug function (debugFunc)...')
        if debug:
            debugFunc()

        logging.info('Elapsed time + str(time.time() - startTime) : ' + str(time.time() - startTime))


        if   'dog' in   detectedClasses :  return "dog"
        elif 'cat' in   detectedClasses :  return "cat"
        else                            :  return "NA"



    def getObjectCoordinates(self):

        if self._siftBox != None:
            return self._siftBox
        else:
            logging.warning('No cats detected - no positions found, meaningless call')


# TODO: Detect how many cats are present to determine amount of food.

# When dogs are present output: 'dog'.
# When both cats and dogs are present output: 'dog'.
# When none are present: 'NA'

# TODO: Put threshold for detection.
# a = NeuralNetwork(debugMode=True)
# im = cv2.imread('wallpaper.jpg')
# a.classifyCatDog(im)
# print('APRTILEasdasd')
