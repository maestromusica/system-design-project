import cv2
import numpy as np
import cPickle as pickle
from Vision import Vision
from base import Box
import json

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
        y = self.modelY.predict(centroid[0])
        x = self.modelX.predict(centroid[1]) - 60
        return (x,y)
    
    def getPickPoints(self,boxes):
        pickPoints = []
        for b in boxes:
            pickPoints.append(self.AdaptPoints(b.centroid))
        return pickPoints
            
    def do_stuff(self):
        while True:
           image, boxes = self.vision.go()
           cv2.imshow('frame',image)
           pickPoints = self.getPickPoints()
           if cv2.waitKey(10) and 0xFF == 32:
               break
        cv2.destroyAllWindows()

adaptor = Adaptor()
adaptor.do_stuff()
