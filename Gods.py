import cv2
import numpy as np
import Fairies as fs
import MaskCalibrator as mc

'''

method: calibrateCamera() :: NO INPUT
                             runs the chessboard program and calibration stuff
                             RETURNS calibration dict
                             {'optmtx':[[float]],'mtx':[[float]],'distcoeffs':[]}
                             POSSIBLE EXTENSION
                             input to start with preconfigued calibration
                             able to see workspace with current calibration
                             able to see workspace with new calibration before saving
                             controls to run calibration with chessboard, see result, 
                             save(return matrix or None), exit

method: calibrateMaskVals() :: NO INPUT
                               runs the calibrator program with trackbars etc
                               RETURNS calibration dict
                               {'colourname':{'Erode':int,'Dilate':int,'H_min':int,'H_max':int,
             'S_min':int,'S_max':int,'V_min':int,'V_max':int,'blur':int}}

'''

class CamCalibrator(object):

    def __init__(self,boardSize):
        #size of the board we are using
        self.boardSize = boardSize
        #termination criteria
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,30,0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.objp = np.zeros((boardSize[0]*boardSize[1],3), np.float32)
        self.objp[:,:2] = np.mgrid[0:boardSize[0],0:boardSize[1]].T.reshape(-1,2)

    def calibrate(self):
        optmtx, mtx, dist = self.runChess()
        if optmtx is not None:
            return {'optmtx':optmtx,'mtx':mtx,'distcoeffs':dist}
        else:
            return None

    def runChess(self):
    
        count = 0
        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.
        capture = False
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            # Converting to gray scale
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, self.boardSize,None)

            # If found, add object points, image points 
            if(ret == True and capture == True):
                objpoints.append(self.objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), self.criteria)
                imgpoints.append(corners)
                #draw and display the corners
                cv2.drawChessboardCorners(frame,self.boardSize, corners2, ret)
                cv2.imshow('detected-corners',frame)
                count += 1
                capture = False

                if count == 10:
                    break
            
            cv2.imshow('frame',frame)

            k = cv2.waitKey(1)
            if (k == ord('c')):
                capture = not capture
            elif( k ==  32):
                break

        cap.release()
        cv2.destroyAllWindows()

        if count == 10:
            ret, mtx, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
            h,  w = frame.shape[:2]
            optmtx, _ = cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
            return optmtx, mtx, dist
        else:
            return None, None, None

class MaskValueCalibrator(object):

    def __init__(self):
        #nothing to initialise yet, but could be in future
        self.hi = 'hello'

    def calibrate(self):
        #runs the mask value calibrator
        self.hi = 'bye'
        return mc.run()



class ImageProcessor(object):

    def __init__(self,camParams,workspace,maskVals,quality=0.5):

        self.camParams = camParams
        self.wsFinder = fs.wsFinder(camParams,workspace)
        self.maskFinder = fs.maskFinder(maskVals)
        self.boxFinder = fs.boxFinder(quality)

    #returns dict of boxes {colorName:[boxObject]}
    def process(self, img):

        #changes the image to just the workspace
        wsImg = self.wsFinder.find(img)
        #gets mask images for the workspace image
        #masks :: {'colorname':[[image]]} dict of mask images (matricies?) by name of color (string)
        masks = self.maskFinder.find(wsImg)
        #finds the boxes in the workspace
        #boxes :: {'colorname':[box]} dict of lists of boxes (box object type) by name of color (string)
        image, boxes = self.boxFinder.find(wsImg,masks)
        #unpack the boxes to return in a more universal format
        unpacked_boxes = self.unpack(boxes)
        return image, boxes

    def unpack(self,boxes):
        unpacked_boxes = []
        for c, boxlist in boxes.items():
            for box in boxlist:
                unpacked_boxes.append(box.getDetails())
        
        return unpacked_boxes

