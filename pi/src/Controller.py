#!/usr/bin/python3
import Server
import Constants

'''
Server side

Currently under test...

'''

constants   = Constants.getConstants()

videoClient   = Server.VideoServer(constants)
# CommandClient = pi.src.Client.CommandClient()
