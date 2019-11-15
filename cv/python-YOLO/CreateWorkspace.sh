#!/bin/bash

mkdir ~/RAM/YOLO
ln ~/RAM/YOLO
cd YOLO

wget https://pjreddie.com/media/files/yolov3-tiny.weights
wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
#wget https://pjreddie.com/media/files/yolov3.weights # performance issues...
