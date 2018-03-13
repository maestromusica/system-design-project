import cv2
import numpy as np
from base import MaskGenerator, ContourExtractor, CornersDetector, Drawer

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
        #self.boxDict = {}

    def createDict(self,centroid,dim,colour,rotation):
        if dim[0] > dim[1]:
            length = dim[0]
            width = dim[1]
        else:
            length = dim[1]
            width = dim[0]
        return {'centroid':centroid,'length':length,'width':width,\
                'colour':colour,'rotation':rotation}
    
    def find(self, img, masks):
        draw = img.copy()
        boxes = []
        for k, m in masks.items():
            cv2.imshow('mask-'+k,m)
            contours = self.contourExtractor.segmentation(m)
            if len(contours) > 0:
                for box, rect in contours:
                    #corners, centroid = self.cornersDetector.detectCorners(img, m, box)
                    #draw = self.drawer.drawBox(img,corners,centroid,'r')
                    angle = rect[2]
                    if(rect[2] < 2 and rect[2] > -10 or (rect[2] > -90 and rect[2] < -80) ):
                        diff_x = 0
                        diff_y = 0
                        for i,b in enumerate(box):
                            for c in box[i+1:]:
                                diff = np.abs(b[0] - c[0])
                                if diff > diff_x:
                                    diff_x = diff
                                diff = np.abs(b[1] - c[1])
                                if diff > diff_y:
                                    diff_y = diff
                        if diff_x > diff_y:
                            angle = 0.00
                        elif diff_y > diff_x:
                            angle = 90.00
                    draw = self.drawer.drawBox(draw,box,np.array(rect[0]),'b')
                    boxes.append(self.createDict(rect[0],rect[1],k,angle))
                    draw = self.drawer.putText(draw,k,len(contours),angle)                    
                #self.boxDict.update({k:boxes})

        return draw, boxes

