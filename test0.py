import cv2
import numpy as np
import cPickle as pickle
import sys
import json
from base import BoxExtractor


def main():

    cap = cv2.VideoCapture(0)
    be = BoxExtractor('picklerick.pkl')

    pts1 = np.float32([[160,0],[410,20],[120,480],[410,480]])
    pts2 = np.float32([[0,0],[200,0],[0,500],[200,500]])

    M = cv2.getPerspectiveTransform(pts1,pts2)



    while True:
       _ , frame = cap.read()


       dst = cv2.warpPerspective(frame,M,(200,500))
       ##cv2.circle(frame, (640,480), 100, (255,255,255) )
       cv2.imshow('frame',frame)

       cv2.imshow('tranformed image',dst)

       f, boxes = be.processImage(dst)
       if boxes is not None:
           print(boxes)
       else:
           print('No boxes')
       cv2.imshow('transformed detectioni',f)
       k = cv2.waitKey(100)
       if k == 32:
           break

    cv2.destroyAllWindows()


main()
