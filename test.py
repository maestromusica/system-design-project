import cv2
import numpy as np
import cPickle as pickle
import sys
import json



def main():

    cap = cv2.VideoCapture(0)


    pts1 = np.float32([[160,0],[410,20],[120,480],[410,480]])
    pts2 = np.float32([[0,0],[200,0],[0,500],[200,500]])

    M = cv2.getPerspectiveTransform(pts1,pts2)



    while True:
       _ , frame = cap.read()




       dst = cv2.warpPerspective(frame,M,(200,500))
       ##cv2.circle(frame, (640,480), 100, (255,255,255) )
       cv2.imshow('frame',frame)

       cv2.imshow('tranformed image',dst)

       cv2.waitKey(100)


main()
