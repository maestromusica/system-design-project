import cv2
import numpy as np


def main(arg):

    # cap = cv2.VideoCapture(0)


    while True:
       # _ , frame = cap.read()
       dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
       x1 = cv2.aruco.drawMarker(dictionary,1,200)
       cv2.imshow('1',x1)
       x2 = cv2.aruco.drawMarker(dictionary,2,200)
       cv2.imshow('2',x2)
       x3 = cv2.aruco.drawMarker(dictionary,3,200)
       cv2.imshow('3',x3)
       x4 = cv2.aruco.drawMarker(dictionary,4,200)
       cv2.imshow('4',x4)
       x5 = cv2.aruco.drawMarker(dictionary,5,200)
       cv2.imshow('5',x5)
       x6 = cv2.aruco.drawMarker(dictionary,6,200)
       cv2.imshow('6',x6)

       k = cv2.waitKey(10)
       if k == 32:
           break

    cv2.destroyAllWindows()


main(0)
