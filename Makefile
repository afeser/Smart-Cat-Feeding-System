PI_SRC=pi/src/

run:
	./RunPi.sh || ./RunServer.sh


buildClient:
	echo "Building client, use 'make run' to run..."
	cp $(PI_SRC)/RunPi.sh ./
	chmod +x RunPi.sh

buildServer:
	echo "Building server"
	cp $(PI_SRC)/RunServer.sh ./
	chmod +x RunServer.sh



build: buildServer buildClient
