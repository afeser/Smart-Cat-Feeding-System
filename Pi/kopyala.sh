#!/bin/bash


mkdir /tmp/RAM/pi
sshfs  pi@192.168.43.219:/home/pi /tmp/RAM/pi

while [ 1 ]
do
	cp CameraDriver.py /tmp/RAM/pi/
	cp ServerClient.py /tmp/RAM/pi/
	sleep 1
done

exit 0

