import cv2
import numpy as np

back = cv2.imread('background1.png',0)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #subtracted = cv2.subtract(gray,back)
    ret, thresh = cv2.threshold(gray,140,255,cv2.THRESH_BINARY)
    subtracted = cv2.subtract(gray, thresh)
    cv2.imshow('frame',frame)
    cv2.imshow('thresh',thresh)
    cv2.imshow('subtracted',subtracted)
    k = cv2.waitKey(5)
    if k == 32:
        break

cv2.destroyAllWindows()
    
