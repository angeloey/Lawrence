import numpy as np
import cv2
import serial
from SerialCommands import *

magnitude = 0
direction = 0
pen = 0

robotX = 0 ## default position and angle of robot, robot must start at this location/oprientation (better solution is CV + fiducials, maybe in V2)
robotY = 0
robotAngle = 0

stepSize = 1.8 # in degrees
wheelRadius = 40    # in mm
wheelCircumference = 2*(np.pi)*wheelRadius
wheelSpaced = 150  # in mm
turnRadius = wheelSpaced/2
turnCircumference = 2*(np.pi)*turnRadius

wheelTurnsPerRotation = turnCircumference / wheelCircumference

stepsPerWheelTurn = 360 / stepSize
stepsPerRotation = wheelTurnsPerRotation * stepsPerWheelTurn

canvasX = 841       #A1 peice of paper (subject to change)
canvasY = 594       #canvas dimensions in mm

def calcVectorDistance(): ## calc distance to next vector, currently in MM for A1 peice of paper, needs scaling for other sizes. linear 1:1 when resizing image to canvas size?
    vectorX = x - robotX
    vectorY = y - robotY
    vectorDistance = np.sqrt(np.square(vectorX)+np.square(vectorY))
    return vectorDistance

def valmap(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def calcAngleToVector(): ## returns degrees to turn in order to face the next vector, measured CLOCKWISE from currently facing direction
    vector = [(x - robotX), (y - robotY)]
    y_axis = [0, 1]
    unit_vector = vector / np.linalg.norm(vector)
    unit_y = y_axis / np.linalg.norm(y_axis)
    dot_product = np.dot(unit_vector, unit_y) ## using dot product, essentially working with "projections"
    angle = np.arccos(dot_product)
    angleInDegrees = 360*angle/(2*np.pi)
    if vector[0]<0: ## this is here to fix the issue that if x-coordinate of vector is negative, arccos effectively computes an angle measured counter clockwise
        angleInDegrees = 360-angleInDegrees ##flip that badboy back to clockwise measurements
    return angleInDegrees

def faceNextPoint(): ## returns steps and direction required to face the next vector
    global robotAngle
    if calcAngleToVector() > 180:                                           ## if turn is more than a 180 degree clockwise turn
        rotateClockwise = 0                                                                 #robot should turn anticlockwise LEFT
        rotateSteps = valmap((360 - calcAngleToVector()),0,360,0,stepsPerRotation)         #steps needed to face next point (360 - anti clockwise turn)
    else:
        rotateClockwise = 1                                                                 #robot should turn clockwise RIGHT
        rotateSteps = valmap(calcAngleToVector(),0,360,0,stepsPerRotation)                  #steps needed to face next point
    robotAngle = calcAngleToVector() ## update global robot angle (should be this angle after turning) DUMB SOLUTION! USE CV and FIDUCIALS!!!!!!!!
    return rotateSteps, rotateClockwise

def stepsToNextPoint(): ## returns the steps required to cover the distance to the next vector
    global robotX; global robotY
    distanceInTurns = calcVectorDistance() / wheelCircumference ## calculate distance in terms of wheel turns (assuming calcVectorDistance retuns value in mm)
    distanceInSteps = distanceInTurns * stepsPerWheelTurn ##translate wheel turns to number of steps required
    robotX = x
    robotY = y ##update global robot x & y positions, (should be this x & y after moving) DUMB SOLUTION! USE CV and FIDUCIALS!!!!!!!!
    return distanceInSteps


imageOriginal = cv2.imread('C:/Users/angel/Desktop/Lenna_(test_image).png')         #read test image lenna
imageGrayscale = cv2.cvtColor(imageOriginal, cv2.COLOR_BGR2GRAY)                                            #convert image to grayscale
imageResized = cv2.resize(imageGrayscale,[594,841])                                                         #Resize image to size of A1 Paper (pixels to mm) 
imageGaussian = cv2.GaussianBlur(imageResized, (5,5), 0)                                                    #Gaussian Blur to Reduce Noise
imageEdged = cv2.Canny(imageGaussian, 100, 200)                                                             #Canny Edge Detection
contours, hierarchy = cv2.findContours(imageEdged, cv2.RETR_CCOMP , cv2.CHAIN_APPROX_TC89_KCOS)             #find countours, approximate chain and save coordiantes (teh shin algorithm)



for c in contours:
    raisePen() # raise the pen

    for i in range(len(c)):
        x, y = c[i][0]
        
        magnitude, direction = (np.rint(faceNextPoint())).astype(int)
        for j in range(magnitude): # turn to face the next point of the contour
            if(direction == 0):
                turnL()
            elif(direction == 1):
                turnR()
        
        steps = (np.rint(stepsToNextPoint())).astype(int)
        for j in range(steps):
            forwards() # travel forwards to the next point of the contour
        
        lowerPen() # lower the pen
        
        
        

