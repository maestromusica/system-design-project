from cv2 import VideoCapture
from base import BoxExtractor
import GlobalParams as gp
import cPickle as pkl

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
        #get values for parameters
        self.camParams = gp.getCamParams(cam)
        self.workspace = gp.getWorkSpace(wkspc)
        self.maskVals = gp.getMaskVals(maskv)
        self.cap = VideoCapture(0)
        self.boxExtractor = BoxExtractor(self.camParams,self.workspace,self.maskVals)

    def go(self):
        
        #take a picture
        img = self.cap.read()
        #process the image and return boxes
        image, boxes = self.boxExtractor.processImage(img)
        #unpack boxes into info we want to return
        return image, boxes

    def calibrateCamera(self):
        cam = Gods.CalibrateCamera()
        data = cam.calibrate()
        filename = raw_input('Enter name for the configuration file: ')
        save(filename,data)

    def calibrateMaskVals(self):
        maskvals = Gods.CalibrateMaskVals()
        data = maskvals.calibrate()
        filename = raw_input('Enter name for the configuration file: ')
        save(filename,data)

    def save(self, filename, data):
        f = open(filename,'w')
        pkl.dump(data,f)
        f.close()
