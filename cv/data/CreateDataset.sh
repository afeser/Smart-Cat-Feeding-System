#!/bin/bash



mkdir -p ~/RAM/YOLO
mkdir -p ~/RAM/SIFT

ln -s ~/RAM/YOLO
ln -s ~/RAM/SIFT


####################################################### YOLO
cd YOLO


#wget -nc https://pjreddie.com/media/files/yolov3-tiny.weights
wget -nc https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
wget -nc https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names


wget -nc https://pjreddie.com/media/files/yolov3.weights # performance issues...


####################################################### SIFT
cd ../SIFT


#wget -nc http://dosya.afeserpi.duckdns.org:8080/dataset/PoncikDataset.zip
#wget -nc http://dosya.afeserpi.duckdns.org:8080/dataset/METUDataset.zip
#wget -nc http://dosya.afeserpi.duckdns.org:8080/dataset/BitirimIkiliDataset.zip
#wget -nc http://dosya.afeserpi.duckdns.org:8080/dataset/frameExamples.zip
#wget -nc http://dosya.afeserpi.duckdns.org:8080/dataset/SIFTDogaUtku.zip
wget -nc http://dosya.afeserpi.duckdns.org:8080/dataset/FacebookDataset13.zip

for f in *.zip
do
	unzip -o $f
done

