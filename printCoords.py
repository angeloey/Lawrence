import cv2
import numpy as np
import matplotlib.pyplot as plt

def calcAngleToVector(): ## returns degrees to turn in order to face the next vector, measured Counter-CLOCKWISE from currently facing direction
    global robotAngle; global robotX; global robotY
    dx = x - robotX
    dy = y - robotY
    angle = np.arctan2(dy, dx)  #radians
    angleInDegrees = angle * 180 / np.pi #degrees from 180 to -180
    angleInDegrees = (angleInDegrees + 360) % 360 # degrees from 0 to 360, 0 = x axis, measured CCW
    angleToTurn = angleInDegrees - robotAngle # actual angle to turn, negative = CW, pos = CCW //trying inverting this
    robotAngle = angleInDegrees ## update global robot angle (should be this angle after turning) DUMB SOLUTION! USE CV and FIDUCIALS!!!!!!!!
    robotX = x
    robotY = y
    return angleToTurn

canvasX = 420
canvasY = 297
robotAngle = 0
robotX = 0
robotY = 0

imageOriginal = cv2.imread('D:/Users/Faith Thompson/Pictures/Arrow.png')         #read test image lenna
imageGrayscale = cv2.cvtColor(imageOriginal, cv2.COLOR_BGR2GRAY)                                            #convert image to grayscale
imageResized = cv2.resize(imageGrayscale,[canvasY,canvasX])                                                 #Resize image to size of A1 Paper (pixels to mm) 
imageGaussian = cv2.GaussianBlur(imageResized, (5,5), 0)                                                    #Gaussian Blur to Reduce Noise
imageEdged = cv2.Canny(imageGaussian, 100, 200)                                                             #Canny Edge Detection
contours, hierarchy = cv2.findContours(imageEdged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)             #find countours, approximate chain and save coordiantes (teh shin algorithm)

cv2.drawContours(imageOriginal, contours, -1, (0,255,0), 1)
imageOriginal[1,1]=(1, 1, 255)
cv2.imshow("poo",imageEdged)
cv2.waitKey(0)

for c in contours:
    #raisePen() # raise the pen
    print("start")
    print(c)
    for i in range(len(c)):
        x, y = c[i][0]
        anglepoo = calcAngleToVector()
        print(anglepoo)
        imageOriginal[y,x]=(1, 1, 255)
        img1 = cv2.cvtColor(imageOriginal,cv2.COLOR_BGR2RGB)
    
    plt.figure(figsize=(10,10))
    plt.imshow(img1, 'gray')
    plt.title("ORIGINAL")
        #plt.show()
    plt.show()
    print("end")


