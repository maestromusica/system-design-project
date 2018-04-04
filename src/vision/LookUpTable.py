#!/usr/bin/env python 
import cv2
import numpy as np
from GlobalParams import GlobalParams 
from Fairies import WorkspaceFinder
import _pickle as pkl

global YPoints
YPoints = []
def printPoint(events,x,y,flags,params):
    global YPoints
    if events == cv2.EVENT_LBUTTONDBLCLK:
        YPoints.append([x,y])
        print('Point is at : ({},{})    len : {}'.format(x,y,len(YPoints)))
    if events == cv2.EVENT_RBUTTONDBLCLK:
        print('Removing : {}'.format(YPoints[-1]))
        del YPoints[-1]

if __name__=='__main__':
    cap = cv2.VideoCapture(1)
    ret , frame = cap.read()
    cv2.imshow('frame',cv2.flip(frame,1))
    cv2.setMouseCallback('frame',printPoint)
    camParams = GlobalParams().getCamParams(None)
    workspace = GlobalParams().getWorkSpace(None)
    pt = WorkspaceFinder(camParams,workspace)
    
    while True:
        _ , frame = cap.read()
        show = pt.find(cv2.flip(frame,1))
        cv2.imshow('frame',show)
        k = cv2.waitKey(10)
        if k == 32:
            break
        if k == ord('s'):
            print('Saving points to pixelCoordinates.pkl')
            f = open('pixelCoordinates.pkl','wb')
            pkl.dump(np.array(YPoints),f)
            f.close()
            break

    cv2.destroyAllWindows()
