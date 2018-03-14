from Parameters import Boxes
import logging
import numpy as np

class Bin(object):

    def __init__(self, binSize):
        self.length = binSize[1]
        self.width = binSize[0]
        #2d array of bools, True is empty, False is full

        self.area = np.ones((self.length,self.width),np.bool_)
        #list of box
        self.boxes_packed = []
        self.corners = [[0,0]]
        self.ws = [0]
        self.ls = [0]

    def inside(self, box, center):
        c0 = center[0]
        c1 = center[1]
        w = box.width + c0
        l = box.length + c1
        center_in = c0 <= self.width and c1 <= self.length
        corner_in =  w <= self.width and l <= self.length
        return center_in and corner_in





class Box(object):


    def __init__(self,box):
        self.colour = box['colour']
        self.weight = Boxes[self.colour]['weight']
        self.centrefrom = np.float32(box['centroid'])
        self.rotation = np.float32(box['rotation'])
        self.rotateto = False
        self.centreto = None
        self.packed = False
        #if self.rotation == 0.00:
        #    self.length = Boxes[self.colour]['w']
        #    self.width = Boxes[self.colour]['l']
        #else:
        self.length = Boxes[self.colour]['l']
        self.width = Boxes[self.colour]['w']
        self.height = Boxes[self.colour]['h']
        self.area = self.length*self.width
        self.volume = self.length*self.width*self.height


    def nearest(self, w, l):
        (dims, _) = Boxes[self.colour]
        #consider choice of priority, length over width why?
        ldiffs = np.abs(dims-l)
        lidx = ldiffs.argmin()
        wdims = np.delete(dims,[lidx])
        wdiffs = np.abs(wdims-w)
        widx = wdiffs.argmin()
        hdims = np.delete(wdims,[widx])
        length, width, height = dims[lidx], wdims[widx], hdims[0]
        return length, width, height
