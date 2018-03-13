
import cv2
from os import path
import numpy as np
import _pickle as pickle
from Vision import Vision
from sklearn.linear_model import LinearRegression

global offset
offset = 0.5
class Adaptor(object):
    def __init__(self,modelfile = 'data/AdapterModels.pkl'):
        dir = path.dirname(path.abspath(__file__))
        self.AdapterX, self.AdapterY = self.loadModels(path.join(dir,modelfile))
        self.thresholdY = 100
    def loadModels(self,filename):
        f = open(filename,'rb')
        modelX = pickle.load(f)
        modelY = pickle.load(f)
        f.close()
        return modelX,modelY

    def calcOffset(self,current,prev):
        offset = 0
        if current.centreto[1] - prev.centreto[1] < self.thresholdY:
            offset = np.float32((current.width + prev.width)/16)
            print(offset)
        return offset
            # This means that the boxes are aligned along their length.
            
    
    def adaptPoints(self, centroid):
        centroid = np.array([list(centroid)],np.int0)
        y = self.AdapterY.predict(centroid)
        x = self.AdapterX.predict(centroid)
        return [x.flatten()[0],y.flatten()[0]]
    def findPickOffsets(self,b):
        if b.rotation == 90:
            #vertical
            offset = b.length*50 - 10
            if offset < 60:
                offset = 60
        else: offset = b.width*50 +25 # horizontal
        return -offset
        
    def adaptBoxes(self,boxes):
        global offset
        adaptedBoxes = []
        for i,b in enumerate(boxes):
            print("OriginalValues : from : {}\t to {}".format(b.centrefrom,b.centreto))
            b.centrefrom = self.adaptPoints(b.centrefrom)
            #b.centrefrom[0] += self.findPickOffsets(b)
            #b.centreto = self.adaptPoints(b.centreto)
            #b['centroid'] = self.adaptPoints(b['centroid']
            #b.centrefrom[0] -= b.width*50
            #if b.centrefrom[0] > 1200:
            #    b.centrefrom[1] += 75
            #    b.centrefrom[0] -= 100
            #if i is not 0:
            #    off = self.calcOffset(b,boxes[i-1])
            #else:
            #    off = 0
            #print("centre before : {}".format(b.centreto))
            #b.centreto[0] = 2*i*offset + b.centreto[0]
            #print("centre after : {}".format(b.centreto))            
            adaptedBoxes.append([b.centrefrom,100*b.centreto,b.rotation,b.colour,b.rotateto])
            #adaptedBoxes.append([b['centroid'],np.array([200,100]),b['rotation']])

        return adaptedBoxes
    
    def transform(self,bins):
        layers = {}
        for i, bin in enumerate(bins):
            layers[i] = self.adaptBoxes(bin.boxes_packed)
        #layers[0] = self.adaptBoxes(bins)
        return layers
