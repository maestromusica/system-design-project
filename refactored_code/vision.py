import cv2
import numpy as np
import ColorObjectTracker as cot
from base import BoxExtractor
import Calibrator


def nothing(x):
    pass

def main():

    filename = Calibrator.main()
    if filename is None:
        filename = 'precision.pkl'

    cap = cv2.VideoCapture(0)
    bx = BoxExtractor(filename)

    while True:
       _ , frame = cap.read()

       cv2.imshow('frame',frame)
       res, boxes = bx.processImage(frame)
       cv2.imshow('result',res)
       print boxes
       k = cv2.waitKey(10)
       if k == 32:
           break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    main()
