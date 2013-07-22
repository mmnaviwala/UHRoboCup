#!/usr/bin/env python

import math
import config
import time

from multiprocessing import Process
from multiprocessing import Pipe

parent, child = Pipe(True)

# This is used to move current location to the a new position relative to
# the current position.
#   @param: x - meters forward
#   @param: y - meters to either side (left is positive)
#   @param: theta - the dirction to be facing at the end of the movement
#       the units are in radians ranging from pi to - pi
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
#    a.start()
    while(isArrived(x,y) != True):
        config.motionProxy.move(v1[0],v1[1],v1[2])
#        v1 = parent.recv()
    config.motionProxy.moveTo(0,0,theta)


# This function is meant to correct the variations between the theortical
#   world in which the programing moves in and actual real world conditions
# NOTE: This function does not work.
def autoCorrect(x,y):
    time.sleep(2)
    while(config.motionProxy.walkIsActive()):
        tolerance = .01
        p1 = config.motionProxy.getRobotPosition(True)
        p2 = config.motionProxy.getNextRobotPosition()
        v2 = [p2[0]-p1[0],p2[1]-p1[1]]
        if(math.fabs((math.pi - math.atan(v2[1]/v2[0])) - math.atan(y/x)) > tolerance):
            theta = (math.atan2(v2[1],v2[0]))
            if(theta < 0):
                v3 = [math.sin(theta),-math.cos(math.pi + theta),0]
            elif(theta > 0):
                v3 = [math.sin(theta),math.cos(math.pi - theta),0]
            print "Actual Velocity Vector: "
            print v2
            print "Correction Vector"
            print v3
            child.send(v3)
            time.sleep(1)

# This is to figure out if we have arrived at the target location
#    @param: x - wanted absolute x coordinates as per getRobotPosition function
#    @param: y - wanted absolute y coordinates as per getRobotPosition function
def isArrived(x,y):
    tolerance = .01
    current = config.motionProxy.getRobotPosition(True)
    varient = [math.fabs(current[0]-x),math.fabs(current[1]-y),0]
    if((varient[0] < tolerance) & (varient[1] < tolerance)):
        return 1
    else:
        return 0

# Rotates the robot theta radians(ranging from -pi to pi)
def rotate(theta):
    current = config.motionProxy.getRobotPosition(True)
    config.motionProxy.moveTo(0,0,current+theta)
