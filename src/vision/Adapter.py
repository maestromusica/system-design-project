import cv2
from os import path
import numpy as np
import _pickle as pickle
from Vision import Vision
from sklearn.linear_model import LinearRegression


class Adaptor(object):
    def __init__(self,modelfile = 'data/AdapterModels.pkl'):
        dir = path.dirname(path.abspath(__file__))
        self.AdapterX, self.AdapterY = self.loadModels(path.join(dir,modelfile))
    def loadModels(self,filename):
        f = open(filename,'rb')
        modelX = pickle.load(f)
        modelY = pickle.load(f)
        f.close()
        return modelX,modelY

    def adaptPoints(self, centroid):
        centroid = np.array([list(centroid)],np.int0)
        y = self.AdapterY.predict(centroid)
        x = self.AdapterX.predict(centroid)
        return (x.flatten()[0],y.flatten()[0])
    
    def adaptBoxes(self,boxes):
        adaptedBoxes = []
        for b in boxes:
            #print("OriginalValues : from : {}\t to {}".format(b.centrefrom,b.centreto))
            #b.centrefrom = self.adaptPoints(b.centrefrom)
            #b.centreto = self.adaptPoints(b.centreto)
            b['centroid'] = self.adaptPoints(b['centroid'])
            
            #adaptedBoxes.append([b.centrefrom,b.centreto])
            adaptedBoxes.append([b['centroid'],np.array([200,100]),b['rotation']])

        return adaptedBoxes
    
    def transform(self,bins):
        layers = {}
        #for i, bin in enumerate(bins):
        #    layers[i] = self.adaptBoxes(bin.boxes_packed)
        layers[0] = self.adaptBoxes(bins)
        return layers
