import cv2
import numpy as np

# Creating nothing function
def nothing(x):
    pass

# Creating trackbars
cv2.namedWindow('HSV')
cv2.createTrackbar('H','HSV',0,180,nothing)
cv2.createTrackbar('S','HSV',0,255,nothing)
cv2.createTrackbar('V','HSV',0,255,nothing)
cv2.createTrackbar('Erode','HSV',0,5,nothing)
cv2.createTrackbar('Dilate','HSV',0,5,nothing)

# Reading photograpj
#img = cv2.imread('object0.png')

# Converting to HSV colorspace
#hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

# Creating a square kernel
kernel = np.ones((5,5),np.uint8)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()   
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # getting values from trackbar
    h = cv2.getTrackbarPos('H','HSV')
    s = cv2.getTrackbarPos('S','HSV')
    v = cv2.getTrackbarPos('V','HSV')
    e = cv2.getTrackbarPos('Erode','HSV')
    d = cv2.getTrackbarPos('Dilate','HSV')
    
    lower = np.array([h,s,v])
    higher = np.array([h+20,255,2550])

    mask = cv2.inRange(hsv,lower,higher)
    mask = cv2.erode(mask,kernel,iterations=e)
    mask = cv2.dilate(mask,kernel,iterations=d)

    cv2.imshow('mask',mask)
    cv2.imshow('img',frame)

    k = cv2.waitKey(10)
    if k == 32:
        break
print('Last HSV values = [{},{},{}] and erode/dilate = [{},{}]'
          .format(h,s,v,e,d))
    
cv2.destroyAllWindows()



