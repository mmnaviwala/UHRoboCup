#!/usr/bin/env python

import math
import config
import time

from multiprocessing import Process
from multiprocessing import Pipe

parent, child = Pipe(True)

def move(x,y,theta):
    current = config.motionProxy.getRobotPosition(True)
    print "Initial Location: "
    print current
    m_v1 = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
    print "Magnitude: "
    print m_v1
    v1 = [x/m_v1,y/m_v1,0]
    print "Normalized Path Vector: "
    print v1
#    config.motionProxy.moveTo(0,0,math.atan((y-current[1])/(x-current[0])))
    a = Process(target=autoCorrect, args=(v1[0],v1[1]))
    a.start()
    while(isArrived(x,y) != True):
        config.motionProxy.move(v1[0],v1[1],v1[2])
        v1 = parent.recv()
#    config.motionProxy.moveTo(0,0,theta)

def autoCorrect(x,y):
    time.sleep(2)
    while(config.motionProxy.walkIsActive()):
        tolerance = .01
        v2 = None
        while(v2 == None):
            try:
                v2 = config.motionProxy.getRobotVelocity()
            except:
                pass
        print "Actual Velocity Vector: "
        print v2
        m_v2 = math.sqrt(math.pow(v2[0], 2) + math.pow(v2[1], 2))
        if(m_v2 != 0):
            v2 = [(x-v2[0])/m_v2,(x-v2[1])/m_v2]
            varient = [1-math.fabs((x-v2[0])/(x+v2[0])),
                1-math.fabs((y-v2[1])/(y+v2[1]))]
            v3 = [0,0,0]
            print "Variation of Path: "
            print varient
            if((varient[0] > tolerance) | (varient[1] > tolerance)):
#                if(varient[0] > tolerance):
#                    v3[0] = -v2[0]
                if(varient[1] > tolerance):
                    v3[1] = -v2[1]
                print "Correction Vector"
                print v3
                child.send(v3)
                time.sleep(1)
                v3 = [x,y,0]
                child.send(v3)

def isArrived(x,y):
    tolerance = .01
    current = config.motionProxy.getRobotPosition(True)
    varient = [math.fabs((current[0]-x)/(current[0]+x)),
        math.fabs((current[1]-y)/(current[1]+y)),
        0]
    if((varient[0] < tolerance) & (varient[1] < tolerance)):
        return 1
    else:
        return 0
    
def rotate(theta):
    config.motionProxy.moveTo(0,0,theta)
