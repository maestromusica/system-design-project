import _pickle as pkl
import logging
import numpy as np
from time import time
from Containers import Bin, Box
import Parameters
import Packer
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

#logging debug stuff
LOGLEVEL = logging.DEBUG
#LOGLEVEL = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s', level=LOGLEVEL)


##everything goes width length


class StackingAlgorithm(object):

    def __init__(self, boxes, binSize, alg):
        self.timestamp = time()
        new_boxes = self.getTrueBoxes(boxes)
        exec('self.packer = Packer.'+alg+'(new_boxes, binSize)')
        self.packer.sort()
        self.coords = self.packer.get_xy()
        self.log_error(boxes, new_boxes, alg)
        for sbin in self.packer.bins:
            im = np.array(Image.open('/home/abhishek/system-design-project/src/vision/Container2.png'), dtype=np.uint8)
            fig,ax = plt.subplots(1)
            ax.imshow(im)
            for i, w in enumerate(sbin.area):
                for j, l in enumerate(w):
                    if l:
                        rect = patches.Rectangle((i*100,j*100),100,100,linewidth=1,edgecolor='grey')
                        ax.add_patch(rect)            
            for box in sbin.boxes_packed:
                if box.rotateto:
                    w = box.length
                    l = box.width
                else:
                    w = box.width
                    l = box.length
                rect = patches.Rectangle(((box.centreto[0]-w/2)*100,(box.centreto[1]-l/2)*100),w*100,l*100,linewidth=1,edgecolor='black',facecolor=box.colour)
                ax.add_patch(rect)
            plt.show()

    

        
    #takes a list of dict objects with box information like vision output
    #returns a list of box objects in nonincreasing order
    def getTrueBoxes(self, boxes):
        unsorted_boxes = []
        logging.debug("Boxes passed to getTrueBoxes: {}".format([(box['colour'], box['centroid']) for box in boxes]))
        for b in boxes:
            logging.debug("Making box object for {}, {}".format(b['colour'], b['centroid']))
            box = Box(b)
            logging.debug("Updating unsorted_boxes with {}, {}".format(box.colour, box.centrefrom))
            unsorted_boxes.append(box)
            logging.debug("Contents of unsorted_boxes: {}".format([(box.colour, box.length, box.centrefrom) for box in unsorted_boxes]))
        return unsorted_boxes    
       
        
    def pack(self):
        return self.packer.bins
    

    def box_error(self, boxes, sorted_boxes):
        width_off = 0
        length_off = 0
        for box in boxes:
            for b in sorted_boxes:
                if b.centrefrom[0] == box['centroid'][0] and b.centrefrom[1] == box['centroid'][1]:
                    width_off += np.abs(box['width']-b.width)
                    length_off += np.abs(box['length']-b.length)
        return width_off, length_off
        
    def log_error(self, boxes, new_boxes, alg):
        boxWidthErr, boxLengthErr = self.box_error(boxes, new_boxes)
        error = {'Algorithm':alg, 'Box Width Error':boxWidthErr, 'Box Length Error':boxLengthErr, 'Runtime':time()-self.timestamp}
        packererror = self.packer.get_error()
        error.update(error)
        error.update(packererror)
        logging.debug("Writing error metrics '{}' to 'error_log' file".format(error))
        f = open(str(self.timestamp)+'_error_log','ab+')
        pkl.dump(error,f)
        f.close()
        logging.debug("Written to file.")
        
        
