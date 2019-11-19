#!/usr/bin/python3
import Client
import Constants
import time

'''
Client file on the Pi Zero.

1) Connects to the VideoServer and waits for the requests...
2) Connects to the CommandsServer and waits for commands...
'''

constants   = Constants.getConstants()

videoClient   = Client.VideoClient(constants)
time.sleep(4)
CommandClient = Client.CommandClient(constants)

videoClient.turnOnListenMode()
