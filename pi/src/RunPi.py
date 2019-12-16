#!/usr/bin/python3
import Client
import Constants
import time
import logging

'''
Client file on the Pi Zero.

1) Connects to the VideoServer and waits for the requests...
2) Connects to the CommandsServer and waits for commands...
'''

logging.basicConfig(level=logging.DEBUG)
constants   = Constants.getConstants()

videoClient   = Client.VideoClient(constants)
time.sleep(4)
commandClient = Client.CommandClient(constants)

videoClient.turnOnListenMode()
commandClient.turnOnListenMode()
