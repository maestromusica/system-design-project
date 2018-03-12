import cv2
from base import BoxExtractor
import Gods
from GlobalParams import GlobalParams
import _pickle as pkl
'''this file is the public facing agent of the vision system. no other bits of the vision system should be called by outside forces.

method: go() :: OPTIONAL INPUT as follows
                cam :: string - filename for camera calibrations
                workspace :: string - filename for workspace corner values
                maskvals :: string - filename for mask values
                RETURNS found boxes as a list of dict objects in the format following
                [{'color':'...','centroid':(x,y),'length':float,'width':float,'rotation':float}]

method: calibrateCamera() :: NO INPUT OR RETURNS
                             calls the camera calibration program to run which returns dict:
                                {'optmtx':[[float]],'mtx':[[float]],'distcoeffs':[]}
                             choose a filename to write the calibration parameters to

method: calibrateMasks() :: NO INPUT OR RETURNS
                            calls the colour calibration program to run which returns dict:
                                {'colourname':{'Erode':int,'Dilate':int,'H_min':int,'H_max':int,
             'S_min':int,'S_max':int,'V_min':int,'V_max':int,'blur':int}}
                            choose a filename to write the masks to

method: save() :: saves data to a pickle file
                  INPUT filename :: string
                        data :: dict of data to save
                  NO RETURNS
'''

class Vision(object):

    def __init__(self,cam=None,wkspc=None,maskv=None):

        gp = GlobalParams()
        #get values for parameters
        self.camParams = gp.getCamParams(cam)
        self.workspace = gp.getWorkSpace(wkspc)
        self.maskVals = gp.getMaskVals(maskv)
        self.cap = cv2.VideoCapture(0)
        self.processor = Gods.ImageProcessor(self.camParams,self.workspace,self.maskVals)
        self.camcal = Gods.CamCalibrator(gp.boardSize)
        self.maskcal = Gods.MaskValueCalibrator()


    def go(self):
        ret, img = self.cap.read()
        img = cv2.flip(img,1)
        #cv2.imshow('img',img)
        #cv2.waitKey(0)
        bimg, boxes = self.processor.process(img)
        return bimg, boxes        

    def calibrateCamera(self):
        data = self.camcal.calibrate()
        if data is not None:
            self.save(data)
            if self.usenow():
                self.camParams = data

    def calibrateMaskVals(self):
        data = self.maskcal.calibrate()
        if data is not None:
            self.save(data)
            if self.usenow():
                self.maskVals = data

    def save(self, data):
        filename = input('Enter name for the configuration file: ')
        f = open(filename,'wb')
        pkl.dump(data,f)
        f.close()
        
    def usenow(self):
        yn = input('Would you like to use these settings now? [Y/n]')
        if yn.lower() == 'n':
            return False
        else: return True
