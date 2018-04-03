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
        self.stats = {self.algorithm:{'Runtime for Boxes':[],'Max Density': 0},self.currentPallet.pid:{'Algorithm':self.algorithm,'Box Sort Method':self.box_sort,'Boxes Packed':0,'Box Width Error':0,'Box Length Error':0}}



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
        w_off = 0.0
        l_off = 0.0
        for b in boxes:
            box = Box(b)
            w_off += np.abs(b['width'] - box.width)
            l_off += np.abs(b['length'] - box.length)
            new_boxes.append(box)
        return (w_off, l_off), new_boxes


    def pack(self, boxes):
        timestamp = time()
        box_error, new_boxes = self.getTrueBoxes(boxes)
        self.currentPallet.add_sweep(new_boxes)
        self.packer.sort(new_boxes)
        self.log_error(timestamp, box_error, len(new_boxes))
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

        self.stats[self.currentPallet.pid] = {'Algorithm':self.algorithm, 'Box Sort Method':self.box_sort, 'Boxes Packed':0,'Box Width Error':0,'Box Length Error':0}


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

    def log_error(self, timestamp, box_error, num_boxes):
        #time alg started, total box error, number of boxes sorted
        self.stats[self.algorithm]['Runtime for Boxes'].append((time()-timestamp, num_boxes))
        packer_error = self.packer.get_error()
        self.stats[self.algorithm]['Max Density'] = max(self.stats[self.algorithm]['Max Density'], max([v for k,v in packer_error['Density'].items()]))

        self.stats[self.currentPallet.pid]['Boxes Packed'] += num_boxes
        self.stats[self.currentPallet.pid]['Box Width Error'] += box_error[0]
        self.stats[self.currentPallet.pid]['Box Length Error'] += box_error[1]
        self.stats[self.currentPallet.pid]['Bins Expected'] = packer_error['Bins Expected']
        self.stats[self.currentPallet.pid]['Bins Used'] = packer_error['Bins Used']
        self.stats[self.currentPallet.pid]['Density'] = packer_error['Density']
        self.stats[self.currentPallet.pid]['Free Space'] = packer_error['Free Space']


    def displayStats(self,algs=[], pals=[]):
        best_density = (0.0,[])
        best_runtime = (float('inf'),'None', (0,0))
        for k, v in self.stats.items():
            if len(k)<32:
                runtime = sum([t for (t,_) in v['Runtime for Boxes']])
                total_boxes = sum([b for (_,b) in v['Runtime for Boxes']])
                if runtime/len(v['Runtime for Boxes']) < best_runtime[0]:
                    best_runtime = (runtime/len(v['Runtime for Boxes']),k, runtime, total_boxes)
                if k in algs:
                    print('Algorithm: '+k)
                    print('    Total Runtime: {}s over {} boxes'.format(runtime,total_boxes))
                    print('    Average Time Per Box: {}s'.format(runtime/total_boxes))
                    print('    Maximum Density Achieved: {}% packed'.format(v['Max Density']))

            elif len(k) == 32:
                if k in pals:
                    print('Pallet {}: Packed by {} and sorted by {}'.format(k,v['Algorithm'],v['Box Sort Method']))
                    b = v['Boxes Packed']
                    print('    {} boxes packed onto {} levels'.format(b,v['Bins Used']))
                    print('    {} levels expected'.format(v['Bins Expected']))
                    print('    Average Box Width Error: {} units, Average Box Length Error {} units'.format(v['Box Width Error']/b, v['Box Length Error']/b))
                for i in range(v['Bins Used']):
                    if k in pals:
                        print('    Level {}:'.format(i))
                        print('        Density: {}% packed'.format(v['Density'][i]))
                        print('        Free Space: {} sq units'.format(v['Free Space'][i]))
                    if v['Density'][i] > best_density[0]:
                        best_density = (v['Density'][i], [v['Algorithm']+' with '+v['Box Sort Method']+' on Pallet '+str(k)+' Level '+str(i)])
                    elif v['Density'][i] == best_density[0]:
                        best_density[1].append(v['Algorithm']+' with '+v['Box Sort Method']+' on Pallet '+str(k)+' Level '+str(i))
                    

        print('Best Average Runtime: {}s by {} with a total of {}s over {} boxes'.format(best_runtime[0],best_runtime[1],best_runtime[2], best_runtime[3]))
        print('Best Density: {} by the following -'.format(best_density[0]))
        for bd in best_density[1]:
            print('    {}'.format(bd))
            
    def saveStats(self):
        statsPath = os.path.join(os.path.dirname(__file__), './algstats', str(time()))
        f = open(statsPath,'wb+')
        pickle.dump(self.stats, f)
        f.close()
