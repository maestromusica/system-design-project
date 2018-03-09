import cPickle as pkl
import logging
import numpy as np
from time import time
from Containers import Bin, Box
import Parameters
import Packer

#logging debug stuff
LOGLEVEL = logging.DEBUG
LOGLEVEL = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s', level=LOGLEVEL)


##everything goes width length


class Algorithm(object):

    def __init__(self, boxes, binSize, alg):
        self.timestamp = time()
        #new_boxes = self.getTrueBoxes(boxes)
        exec('self.packer = Packer.'+alg+'(boxes, binSize)')
        self.packer.sort()
        self.coords = self.packer.get_xy()
        self.log_error(boxes, new_boxes, alg)
    

    def pack(self):
        return self.packer.bins
    
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
       
        
        
    def calculate_waste(self):
        total_area_available = np.float32(0)
        total_area_packed = np.float32(0)
        for b in self.packer.bins:
            total_area_available += b.length*b.width
            for pb in b.boxes_packed:
                total_area_packed += pb.area
        error = np.abs(total_area_available - total_area_packed)
        return error

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
        unused_area = self.calculate_waste()
        boxWidthErr, boxLengthErr = self.box_error(boxes, new_boxes)
        error = {'Algorithm':alg,'Unused Area':unused_area, 'Width Error':boxWidthErr, 'Length Error':boxLengthErr, 'Runtime':time()-self.timestamp}
        error.update(self.packer.get_error())
        logging.debug("Writing error metrics '{}' to 'error_log' file".format(error))
        f = open(str(self.timestamp)+'_error_log','a+')
        pkl.dump(error,f)
        f.close()
        logging.debug("Written to file.")
        
        
