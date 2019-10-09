#!/bin/bash


mkdir -p /tmp/RAM/pi
sshfs  pi@192.168.43.219:/home/pi /tmp/RAM/pi

while [ 1 ]
do
	mkdir -p /tmp/RAM/pi/Test
	cp CameraDriver.py /tmp/RAM/pi/Test/
	cp ServerClient.py /tmp/RAM/pi/Test/
	sleep 1
done

exit 0

