from Containers import Bin
from Parameters import offset
import logging
import numpy as np

class BPOF(object):

    def __init__(self, boxes, binSize):
        self.binSize = binSize
        #list of bin objects
        self.boxes = sorted(boxes, key=lambda box: (box.length,box.width))
        self.boxes.reverse()
        logging.debug("Contents of sorted boxes: {}".format([(box.colour, box.length, box.centrefrom) for box in self.boxes]))
        self.bins = []
        L = self.compute_L()
        while L > 0:
            self.bins.append(Bin(self.binSize))
            L -= 1

        
    def get_xy(self):
        coord_sets = []
        for b in self.bins:
            coords = []
            for box in b.boxes_packed:
                coords.append((box.centrefrom,box.centreto))
            coord_sets.append(coords)
        return coord_sets
            
    def sort(self):
        #PHASE ONE
        n_packed = 0
        bxs = len(self.boxes)
        bns = len(self.bins)
        rtl = False
        logging.debug("PHASE ONE:")
        for box in self.boxes:
            i = 0
            while i < bns:
                logging.debug("######Packing to bin {}#######".format(i))
                if self.pack(self.bins[i],box,rtl):
                    n_packed += 1
                    i = bns
                else: i += 1
        
        #PHASE TWO
        logging.debug("PHASE TWO:")
        i = 0
        n_prev = n_packed
        while n_packed < bxs:
            try:
                logging.debug("n_packed: {}".format(n_packed))
                n_fail = 0
                rtl=True
                while n_fail < 2:
                    for box in [box for box in self.boxes if not box.packed]:
                        logging.debug("in second while loop, about to pack into bin {}, nfail={}, rtl={}".format(i,n_fail,rtl))
                        if self.pack(self.bins[i], box, rtl):
                            n_packed += 1
                    if n_packed == n_prev:
                        n_fail += 1
                        logging.debug("added 1 to nfail: {}".format(n_fail))
                    n_prev = n_packed
                    logging.debug("change directions rtl:{} to not rtl:{}".format(rtl,not rtl))
                    rtl = not rtl
                i+=1
                logging.debug("now on bin {}".format(i))
            except IndexError:
                self.bins.append(Bin(self.binSize))
                logging.debug("ADDED NEW BIN!!!!!!!!!!!!!!!!!!!!")

    def compute_L(self):
        total_area = np.float32(0)
        bin_area = np.float32(self.binSize[0]*self.binSize[1])
        logging.debug("Type check total_area: {}, bin_area: {}".format(total_area.__class__, bin_area.__class__))
        for box in self.boxes:
            total_area += box.area
        L = np.int8(np.ceil(total_area/bin_area))
        logging.debug("Type check L: {}".format(L.__class__))
        return L


    def pack(self, con, box, rtl):
        logging.debug("Packing Box:: Colour: {}, Centre: {}, Length: {}, Width, {}".format(box.colour,box.centrefrom,box.length,box.width))
        cols = range(0,np.int8(con.width-box.width+1-offset))
        logging.debug("Cols Range Before Reverse: {}".format(cols))
        if rtl: cols.reverse()
        logging.debug("Cols Range After Reverse: {}".format(cols))
        for i in range(0,np.int8(con.length-box.length+1-offset)):
            for j in cols:
                logging.debug("Packing from corner: {},{} with rtl: {}".format(j,i,rtl))
                if np.all(con.area[i:np.int8(i+box.length)+offset,j:np.int8(j+box.width)+offset]):
                    logging.debug("Packing in area: \n{}".format(con.area[i:np.int8(i+box.length+offset),j:np.int8(j+box.width+offset)]))
                    con.area[i:np.int8(i+box.length)+offset,j:np.int8(j+box.width)+offset] = False
                    vec = np.float32([box.width/2,box.length/2])
                    logging.debug("Box Vector: {}".format(vec))
                    box.centreto = np.float32([j+offset/2,i+offset/2]) + vec
                    logging.debug("Centre Point: {}".format(box.centreto))
                    con.boxes_packed.append(box)
                    box.packed = True
                    return box.packed
        return box.packed

            

    def get_error(self):
        L = self.compute_L()
        L_calc = len(self.bins)
        return {'Bins Expected':L,'Bins Used':L_calc}
        
        

