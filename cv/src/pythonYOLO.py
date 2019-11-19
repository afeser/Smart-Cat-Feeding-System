import cv2
import numpy as np
import time


def classifyCatDog(frame):
    
    # Load YOLO

    net = cv2.dnn.readNet('../data/YOLO/yolov3.weights', "../data/YOLO/yolov3.cfg")
    classes = []

    with open('../data/YOLO/coco.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Preprocessing
    # TODO - garip garip parametreler yaa...
    # blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0,0,0), True, crop=False)

    # Gerisini yapistirdim gereksiz detayliydi..

    font = cv2.FONT_HERSHEY_PLAIN
    starting_time = time.time()

    height, width, channels = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.1:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.3)
    
#     for c in indexes:
        
#         print(classes[class_ids[c]])
        
#     return None
    
    list1 = []
    
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            list1.append(label)
            confidence = confidences[i]
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, color, 3)
          # print(confidences)
          # print(label)
    
    elapsed_time = time.time() - starting_time
    # fps = frame_id / elapsed_time
    cv2.putText(frame, "TIME: " + str(round(elapsed_time, 2)), (10, 50), font, 4, (0, 0, 0), 3)
    cv2.imwrite("Image.jpg", frame)

    print(list1)
    list2 = ['cat','dog']
    
    if 'dog' in list1 :  return "dog"
    elif 'cat' in list1: return "cat"
    else : return "NA"
 

# When cat is present output: 'cat'.

# TODO: Detect how many cats are present to determine amount of food.

# When dogs are present output: 'dog'.
# When both cats and dogs are present output: 'dog'.
# When none are present: 'NA'

# TODO: Put threshold for detection.


