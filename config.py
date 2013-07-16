#!/usr/bin/env python

from naoqi import ALProxy

# Atleast for now start all proxies in this file and make them universal variables
motionProxy = ALProxy("ALMotion","127.0.0.1",9559)
videoProxy = ALProxy("ALVideoDevice","127.0.0.1",9559)
speechProxy = ALProxy("ALTextToSpeech","127.0.0.1",9559)
