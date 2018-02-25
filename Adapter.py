import cv2
import numpy as np
import cPickle as pickle
from Vision import Vision
from base import Box
from sklearn.linear_model import LinearRegression


class Adaptor(object):
    def __init__(self,modelfile = 'AdapterModels.pkl'):
        self.vision = Vision()
        self.AdapterX, self.AdapterY = self.loadModels(modelfile)
    def loadModels(self,filename):
        f = open(filename)
        modelX = pickle.load(f)
        modelY = pickle.load(f)
        f.close()
        return modelX,modelY

    def AdaptPoints(self, centroid):
        print(centroid)
        y = self.AdapterY.predict(centroid[0])
        x = self.AdapterX.predict(centroid[1]) - 100
        return (x,y)

    def getPickPoints(self,boxes):
        pickPoints = []
        for b in boxes.keys():
            box = boxes[b]
            for bo in box:
                pickPoints.append(self.AdaptPoints(bo.centroid))
        return pickPoints
            
    def do_stuff(self):
           image, boxes = self.vision.go()
           cv2.imshow('frame',image)
           pickPoints = self.getPickPoints(boxes)
           return pickPoints

adaptor = Adaptor()
adaptor.do_stuff()
