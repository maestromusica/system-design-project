import logging
import numpy as np
from time import time
from Containers import Bin, Box, Pallet
import Packer
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import uuid
import pickle
import os

#logging debug stuff
LOGLEVEL = logging.DEBUG
LOGLEVEL = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s', level=LOGLEVEL)


##everything goes width length


class StackingAlgorithm(object):

    def __init__(self, binSize, alg, box_sort=None):
        self.algorithm = alg
        self.binSize = binSize
        self.box_sort = box_sort or 'WEIGHT'
        self.currentPallet = Pallet(uuid.uuid4().hex,self.binSize,self.algorithm,self.box_sort)
        exec('self.packer = '+self.currentPallet.string)
        self.stats = {self.algorithm:{'Runtime for Boxes':[],'Max Density': 0},self.currentPallet.pid:{'Algorithm':self.algorithm,'Box Sort Method':self.box_sort,'Boxes Packed':0}}



    def showLevels(self):
        for sbin in self.packer.bins:
            im = np.array(Image.open('Container2.png'), dtype=np.uint8)
            fig,ax = plt.subplots(1)
            ax.imshow(im)
            for box in sbin.boxes_packed:
                if box.rotateto:
                    w = box.length
                    l = box.width
                else:
                    w = box.width
                    l = box.length
                rect = patches.Rectangle(((box.centreto[1]-l/2)*100,(box.centreto[0]-w/2)*100),l*100,w*100,linewidth=1,edgecolor='black',facecolor=box.colour)
                ax.add_patch(rect)
        plt.show()

    def getTrueBoxes(self, boxes):
        new_boxes = []
        for b in boxes:
            box = Box(b)
            new_boxes.append(box)
        return new_boxes


    def pack(self, boxes):
        timestamp = time()
        new_boxes = self.getTrueBoxes(boxes)
        self.currentPallet.add_sweep(new_boxes)
        self.packer.sort(new_boxes)
        self.log_error(timestamp, len(new_boxes))
        for bin in self.packer.bins:
            for box in bin.boxes_packed:
                box.newBox = False
        for box in self.currentPallet.sweeps[-1]:
            box.newBox = True
        self.savePallet()
        return (self.currentPallet.pid, self.packer.bins)

    def savePallet(self):
        self.currentPallet.stats = self.stats[self.currentPallet.pid]
        palletPath = os.path.join(os.path.dirname(__file__), './pallets', self.currentPallet.pid)
        f = open(palletPath,'wb+')
        pickle.dump(self.currentPallet, f)
        f.close()

    def openNewPallet(self, alg=None, box_sort=None):
        #option to switch algorithms
        if alg is not None:
            self.algorithm = alg
        try:
            bool(self.stats[self.algorithm])
        except KeyError:
            self.stats[self.algorithm] = {'Runtime for Boxes':[],'Max Density': 0}
        #opens a new pallet and switches to it
        if box_sort is not None:
            self.box_sort = box_sort
        self.currentPallet = Pallet(uuid.uuid4().hex,self.binSize,self.algorithm,self.box_sort)
        exec('self.packer = '+self.currentPallet.string)

        self.stats[self.currentPallet.pid] = {'Algorithm':self.algorithm, 'Box Sort Method':self.box_sort, 'Boxes Packed':0}


    def switchToPallet(self,p):
        #switches to a different pallet
        #CHANGE THIS NEXT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        try:
            palletPath = os.path.join(os.path.dirname(__file__), './pallets', p)
            f = open(palletPath,'rb')
            self.currentPallet = pickle.load(f)
            f.close()
            self.algorithm = self.currentPallet.alg
            exec('self.packer = '+self.currentPallet.string)
            self.binSize = self.packer.binSize
            for boxes in self.currentPallet.sweeps:
                self.packer.sort(boxes)
            try:
                bool(self.stats[self.currentPallet.pid])
            except KeyError:
                self.stats[self.currentPallet.pid] = self.currentPallet.stats
        except FileNotFoundError:
            print('No Such Pallet')

    ##for recording error and such like

    def log_error(self, timestamp, num_boxes):
        #time alg started, total box error, number of boxes sorted
        self.stats[self.algorithm]['Runtime for Boxes'].append((time()-timestamp, num_boxes))
        packer_error = self.packer.get_error()
        self.stats[self.algorithm]['Max Density'] = max(self.stats[self.algorithm]['Max Density'], max([v for k,v in packer_error['Density'].items()]))

        self.stats[self.currentPallet.pid]['Boxes Packed'] += num_boxes
        self.stats[self.currentPallet.pid]['Bins Expected'] = packer_error['Bins Expected']
        self.stats[self.currentPallet.pid]['Bins Used'] = packer_error['Bins Used']
        self.stats[self.currentPallet.pid]['Density'] = packer_error['Density']
        self.stats[self.currentPallet.pid]['Free Space'] = packer_error['Free Space']



            
    def saveStats(self):
        statsPath = os.path.join(os.path.dirname(__file__), './algstats', str(time()))
        f = open(statsPath,'wb+')
        pickle.dump(self.stats, f)
        f.close()
