import cv2
import numpy as np
from base import MaskGenerator, ContourExtractor, CornersDetector, Drawer, Box

#class for finding the workspace out of a big image thing
class wsFinder(object):

    def __init__(self,camParams, ws):
        self.optmtx = camParams['optmtx']
        self.mtx = camParams['mtx']
        self.dist = camParams['distcoeffs']
        #put workspace vals into order points from and to
        From, To = [], []
        for k, v in ws.items():
            From.append(v[0])
            To.append(v[1])
        self.ptsFrom, self.ptsTo = np.float32(From), np.float32(To)
        
        self.wsSize = (ws['BottomRight'][1][0],ws['BottomRight'][1][1])


    def find(self,img):
        #undistort the image
        corrected_image = cv2.undistort(src=img, cameraMatrix=self.mtx, distCoeffs=self.dist, newCameraMatrix=self.optmtx)
        #get perspective transform matrix
        M = cv2.getPerspectiveTransform(self.ptsFrom,self.ptsTo)
        #crop image
        cropped_img = cv2.warpPerspective(corrected_image,M,self.wsSize)
        return cropped_img



#class for finding the masks from the workspace image
class maskFinder(object):

    def __init__(self,maskVals):
        self.maskGenerators = {}
        for k, v in maskVals.items():
            self.maskGenerators.update({k:MaskGenerator(maskVals[k],k)})
        

    def find(self,img):
        masks = {}
        for k, m in self.maskGenerators.items():
            masks.update({k:m.extractMask(img)})
        return masks

#class for finding boxes in the workspace img
class boxFinder(object):
    def __init__(self, quality):
        self.contourExtractor = ContourExtractor()
        self.cornersDetector = CornersDetector(quality=quality)
        self.drawer = Drawer()
        self.boxDict = {}

    def find(self, img, masks):
        draw = img.copy()
        for k, m in masks.items():
            boxes = []
            contours = self.contourExtractor.segmentation(m)
            if len(contours) > 0:
                for box, rect in contours:
                    corners, centroid = self.cornersDetector.detectCorners(img, m, box)
                    draw = self.drawer.drawBox(img,corners,centroid,'r')
                    draw = self.drawer.drawBox(draw,box,np.array(rect[0]),'b')
                    boxes.append(Box(rect[0], rect[1][1],rect[1][0],k,rect[2]))
                self.boxDict.update({k:boxes})
                draw = self.drawer.putText(draw,k,len(boxes))
        return draw, self.boxDict

