#!/usr/bin/python3
import Client
import Constants

'''
Client file on the Pi Zero.

1) Connects to the VideoServer and waits for the requests...
2) Connects to the CommandsServer and waits for commands...
'''

constants   = pi.src.Constants.getConstants()

videoClient   = pi.src.Client.VideoClient()
# CommandClient = pi.src.Client.CommandClient()

videoClient.turnOnListenMode()
