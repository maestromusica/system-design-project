from Parameters import Boxes
import logging
import numpy as np
from Parameters import offset


class Pallet(object):
    def __init__(self,pid,binSize,alg,box_sort):
        self.pid = pid
        self.alg = alg
        self.string = 'Packer.'+alg+'('+str(binSize)+',"'+box_sort+'")'
        self.stats = None
        self.sweeps = []

    def add_sweep(self, boxes):
        self.sweeps.append(boxes)



class Bin(object):

    def __init__(self, binSize):
        self.length = binSize[1]
        self.width = binSize[0]
        self.boxes_packed = []
        self.freeArea = self.length*self.width
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


    def inside_R(self, box, center):
        c0 = center[0]
        c1 = center[1]
        w = box.length + c0
        l = box.width + c1
        center_in = c0 <= self.width and c1 <= self.length
        corner_in =  w <= self.width and l <= self.length
        return center_in and corner_in



class Box(object):


    def __init__(self,box):
        self.colour = box['colour']
        self.weight = Boxes[self.colour]['weight']
        self.length = Boxes[self.colour]['l']+offset
        self.width = Boxes[self.colour]['w']+offset
        self.height = Boxes[self.colour]['h']
        self.area = self.length*self.width
        self.centrefrom = np.array(box['centroid'])
        self.rotatefrom = box['rotation']
        self.rotateto = None
        self.centreto = None
        self.packed = False
        self.newBox = False
        self.sweep = None
        self.vec = np.array([self.width,self.length])


    def corner(self, c):
        if self.packed:
            v = self.vec/2
            if c[0] == 'b':
                v[1]=v[1]*-1
            if c[1] == 'l':
                v[0] = v[0]*-1
            return self.centreto + v
        else: return None
