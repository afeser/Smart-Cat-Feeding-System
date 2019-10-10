#!/bin/bash

piNum=10.42.0.200

rm -rf /tmp/RAM/pi
mkdir -p /tmp/RAM/pi
sshfs  pi@$piNum:/home/pi /tmp/RAM/pi

while [ 1 ]
do
	mkdir -p /tmp/RAM/pi/Test
	cp CameraDriver.py /tmp/RAM/pi/Test/
	cp ServerClient.py /tmp/RAM/pi/Test/
	sleep 1
done

exit 0

