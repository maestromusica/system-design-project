import cv2
import numpy as np
import Fairies as fs

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

class CalibrateCamera(object):

    def __init__(self):

    def calibrate(self):
    #runs the camera calibrator
        return params

class CalibrateMaskVals(object):

    def __init__(self):

    def calibrate(self):
    #runs the mask value calibrator
        return params

class ProcessImage(object):

    def __init__(self,camParams,workspace,maskVals):

    #returns dict of boxes {colorName:[boxObject]}
    def process(self, img):
        return boxes
