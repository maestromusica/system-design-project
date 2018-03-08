import cv2
from os import path
import numpy as np
import _pickle as pickle
from Vision import Vision
from base import Box
from sklearn.linear_model import LinearRegression


class Adaptor(object):
    def __init__(self,modelfile = 'data/AdapterModels.pkl'):
        self.vision = Vision()
        dir = path.dirname(path.abspath(__file__))
        self.AdapterX, self.AdapterY = self.loadModels(path.join(dir,modelfile))
    def loadModels(self,filename):
        f = open(filename,'rb')
        modelX = pickle.load(f)
        modelY = pickle.load(f)
        f.close()
        return modelX,modelY

    def AdaptPoints(self, centroid):
        centroid = np.array([list(centroid)],np.int0)
        y = self.AdapterY.predict(centroid)
        x = self.AdapterX.predict(centroid) - 100
        return (x,y)

    def getPickPoints(self,boxes):
        picks = {}
        for b in boxes.keys():
            box = boxes[b]
            pickPoints = []
            for bo in box:
                pickPoints.append(self.AdaptPoints(bo.centroid))
            picks[b] = pickPoints
            
        return picks
            
    def do_stuff(self):
           image, boxes = self.vision.go()
           #cv2.imshow('frame',image)
           pickPoints = self.getPickPoints(boxes)
           return image, pickPoints

adaptor = Adaptor()
adaptor.do_stuff()
