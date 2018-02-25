import cv2
import numpy as np
import GlobalParams
from base import PerspectiveTransform

global YPoints
YPoints = []
def printPoint(events,x,y,flags,params):
    global YPoints
    if events == cv2.EVENT_LBUTTONDBLCLK:
        YPoints.append(x)
        print('Point is at : ({},{})'.format(x,y))

if __name__=='__main__':
    cap = cv2.VideoCapture(0)
    ret , frame = cap.read()
    cv2.imshow('frame',cv2.flip(frame,1))
    cv2.setMouseCallback('frame',printPoint)
    camParams = GlobalParams.getCamParams(None)
    workspace = GlobalParams.getWorkSpace(None)
    pt = PerspectiveTransform(camParams,workspace)
    
    while True:
        _ , frame = cap.read()
        show = pt.transform(cv2.flip(frame,1))
        cv2.imshow('frame',show)
        k = cv2.waitKey(10)
        if k == 32:
            break

    cv2.destroyAllWindows()
