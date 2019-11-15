#!/bin/bash

mkdir ~/RAM/YOLO
ln -s ~/RAM/YOLO
cd YOLO

wget -nc https://pjreddie.com/media/files/yolov3-tiny.weights
wget -nc https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
wget -nc https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names


wget -nc https://pjreddie.com/media/files/yolov3.weights # performance issues...

# Samples
wget -nc https://cdn.cnn.com/cnnnext/dam/assets/191024091949-02-foster-cat-exlarge-169.jpg -O cat1.jpg
