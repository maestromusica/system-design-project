import cv2
import numpy as np
from base import MaskGenerator, ContourExtractor, CornersDetector, Drawer

global data

def flipX(point,shape):
    return (int(shape[1] - point[0]-1),int(point[1]))

def findRoi(frame, box):
    min_x = np.min(box[:,0])
    max_x = np.max(box[:,0])
    min_y = np.min(box[:,1])
    max_y = np.max(box[:,1])
    h,w,c = frame.shape
    mask = np.zeros((h,w),np.uint8)
    mask[min_y:max_y, min_x:max_x] = 255
    frame = cv2.bitwise_and(frame,frame,mask=mask)
    return frame
    


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

# class for finding aruco markers
class ArucoFinder(object):
    def __init__(self):
        self.dict_val = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        
    def findMarkers(self,frame):
        
        # Need to flip the frame because aruco markers are not immune to lateral
        # inversion.
        
        flip = cv2.flip(frame,1)        
        res = cv2.aruco.detectMarkers(flip,self.dict_val)

        # if aruco markers found
        if (len(res[0])  > 0):
            for x in range(len(res[1])):
                aruco_id = res[1][x][0]
                # extracting corners
                corners = res[0][x][0]

                # flipping corners again 
                for i,p in enumerate(corners):                    
                    p = flipX(p,frame.shape)
                    corners[i]=p
                # calculating centroid
                centroid = np.sum(corners,axis=0)/4

                return corners, centroid, aruco_id

        return None,None, None


#class for finding boxes in the workspace img
class boxFinder(object):
    def __init__(self, quality):
        self.contourExtractor = ContourExtractor()
        self.cornersDetector = CornersDetector(quality=quality)
        self.arucoFinder = ArucoFinder()
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
            #cv2.imshow('mask-'+k,m)
            contours = self.contourExtractor.segmentation(m)
            if len(contours) > 0:
                for box, rect in contours:
                    # extracting roi
                    roi = findRoi(img,box)
                    cv2.imshow('roi',roi)
                    corners_aruco, centroid_aruco, aruco_id = self.arucoFinder.findMarkers(roi)
                    if corners_aruco is not None:
                        cv2.circle(draw,tuple(corners_aruco[0]),3,(0,255,0),2)
                        cv2.circle(draw,tuple(corners_aruco[1]),3,(0,0,255),2)
                        cv2.circle(draw,tuple(corners_aruco[2]),3,(255,0,0),2)
                        cv2.circle(draw,tuple(corners_aruco[3]),3,(0,255,255),2)
                        cv2.circle(draw,tuple(centroid_aruco),3,(255,255,255),2)
                    else:
                        # if aruco marker not find. Detection is noise. continue with other boxes.
                        # drawing false positives with red.
                        draw = self.drawer.drawBox(draw,box,np.array(rect[0]),'r')
                        continue
                    
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


