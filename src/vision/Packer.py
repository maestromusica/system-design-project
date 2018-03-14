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
        self.error = {"Bins Expected:":L}
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
        '''
        #STUPID CODE

        logging.debug("Packing Box:: Colour: {}, Centre: {}, Length: {}, Width, {}".format(box.colour,box.centrefrom,box.length,box.width))
        cols = list(range(0,np.int8(con.width-box.width+1-offset)))
        logging.debug("Cols Range Before Reverse: {}".format(cols))
        if rtl: cols.reverse()
        logging.debug("Cols Range After Reverse: {}".format(cols))
        for i in range(0,np.int8(con.length-box.length+1-offset)):
            for j in cols:
                logging.debug("Packing from corner: {},{} with rtl: {}".format(j,i,rtl))
                if np.all(con.area[i:np.int8(i+box.length)+offset + 1,j:np.int8(j+box.width)+offset + 1]):
                    logging.debug("Packing in area: \n{}".format(con.area[i:np.int8(i+box.length+offset),j:np.int8(j+box.width+offset)]))
                    con.area[i:np.int8(i+box.length)+offset + 1,j:np.int8(j+box.width)+offset + 1] = False
                    vec = np.float32([box.width/2,box.length/2])
                    logging.debug("Box Vector: {}".format(vec))
                    box.centreto = np.array(([j+offset/2+vec[0],i+offset/2+vec[1]]),dtype=np.float32)# + vec
                    logging.debug("Centre Point: {}".format(box.centreto))
                    con.boxes_packed.append(box)
                    box.packed = True
                    return box.packed

        '''

        '''
        #TRIVIL

        vec = np.float32([box.width/2,box.length/2])

        boxes_packed = con.boxes_packed
        l = 0

        for b in boxes_packed:
            l = l + b.width
        box.centreto = np.array(([l+vec[0],vec[1]]),dtype=np.float32)
        con.boxes_packed.append(box)
        box.packed = True
        '''

        '''
        BETTER ALGORITHM
        for x in con.corners:
            w = x[0]
            l = x[1]
            b_w = box.width
            b_l = box.length
            ## inside bin and bot overlap
            inside = con.inside(box,x)
            overlap = False
            c_w = w + b_w/2
            c_l = l + b_l/2
            for y in con.boxes_packed :
                c0 = y.centreto[0]
                c1 = y.centreto[1]
                if y.width + b_w > 2*( np.abs( c0 - c_w) + 0.001 ) and y.length + b_l > 2*( np.abs( c1 - c_l) + 0.001 ) :
                    overlap = True
                    break
            if inside and not overlap:
                box.centreto = np.array(([ c_w ,c_l ]))
                con.corners.append([w + b_w ,l + b_l] )
                con.corners.append([w ,l + b_l] )
                con.corners.append([w + b_w ,l] )
                con.corners.sort(key=lambda x: x[0] + x[1])
                con.boxes_packed.append(box)
                box.packed = True
                break
        '''

        offset = 0
        for w in con.ws:
            t = False
            for l in con.ls:
                x = [w,l]
                b_w = box.width
                b_l = box.length
                ## inside bin and bot overlap
                inside = con.inside(box,x)
                overlap = False
                c_w = w + b_w/2
                c_l = l + b_l/2
                for y in con.boxes_packed :
                    c0 = y.centreto[0]
                    c1 = y.centreto[1]
                    if y.width + b_w + offset > 2*( np.abs( c0 - c_w) + 0.001 ) and y.length + b_l + offset > 2*( np.abs( c1 - c_l) + 0.001 ) :
                        overlap = True
                        break
                if inside and not overlap:
                    print(con.ws)
                    box.centreto = np.array(([ c_w + offset/2 ,c_l + offset/2 ]))
                    con.ws.append(w + b_w + offset )
                    con.ls.append(l + b_l + offset )
                    con.ws.sort()
                    con.ls.sort()
                    con.boxes_packed.append(box)
                    box.packed = True
                    t = True
                    break
            if t :
                break
        return box.packed



    def get_error(self):
        self.error.update({"Bins Used":len(self.bins)})
        self.calculate_waste()
        return self.error

    def calculate_waste(self):
        total_area_available = np.float32(0)
        total_area_packed = np.float32(0)
        for b in self.bins:
            total_area_available += b.length*b.width
            for pb in b.boxes_packed:
                total_area_packed += pb.area
        self.error.update({"Calculated Area Wastage":np.abs(total_area_available - total_area_packed)})
        tot = 0
        for b in self.bins:
            tot += np.sum(b.area)
        self.error.update({"Measured Area Wastage": tot})



class BPRF(object):
    def __init__(self, boxes, binSize):
        self.binSize = binSize
        self.boxes = sorted(boxes, key=lambda box: (box.area,max(box.width,box.length)))
        self.boxes.reverse()
        logging.debug("Contents of sorted boxes: {}".format([(box.colour, box.length, box.centrefrom) for box in self.boxes]))
        self.bins = []
        L = self.compute_L()
        self.error = {"Bins Expected:":L}
        while L > 0:
            self.bins.append(Bin(self.binSize))
            L -= 1



    def sort(self):
        for box in self.boxes:
            logging.debug("packing box colour: {}, centre: {}".format(box.colour,box.centrefrom))
            score = 0
            packto = (len(self.bins), (0,0), False, score)
            logging.debug("packto: {}".format(packto))
            for i in range(0,len(self.bins)):
                logging.debug("for bin {}".format(i))
                logging.debug("nonrotated")
                poslist = self.getPositions(np.int8(box.width), np.int8(box.length), i)
                if len(poslist) > 0:
                    for pos in poslist:
                        newscore = self.score(pos,np.int8(box.width+offset),np.int8(box.length+offset),i)
                        if  newscore > score:
                            packto=(i, pos, False, newscore)
                            score = newscore
                        logging.debug("packto: {}".format(packto))
                    logging.debug("rotated")
                poslist = self.getPositions(np.int8(box.length),np.int8(box.width),i)
                if len(poslist)>0:
                    for pos in poslist:
                        newscore = self.score(pos,np.int8(box.length+offset),np.int8(box.width+offset),i)
                        if newscore > score:
                            packto=(i, pos, True,newscore)
                            score = newscore
                        logging.debug("packto: {}".format(packto))
            try:
                self.pack(packto[0],packto[1],packto[2], box)
            except IndexError:
                self.bins.append(Bin(self.binSize))
                self.pack(packto[0],packto[1],packto[2], box)

    def pack(self, bn, cor, rot, box):
        #bn is the bin object, cor is tuple bottom left corner, rot is bool rotated or not, box is the box object
        (cw,cl) = cor
        if rot:
            bw = np.int8(box.length+offset)
            bl = np.int8(box.width+offset)
            box.rotateto = rot
        else:
            bw = np.int8(box.width+offset)
            bl = np.int8(box.length+offset)

        self.bins[bn].area[cw:cw+bw,cl:cl+bl] = False
        box.centreto = (cw+bw/2,cl+bl/2)
        self.bins[bn].boxes_packed.append(box)

    #returns a list of coordinates centroid from, to, and whether it needs to be rotated on the way
    def get_xy(self):
        coord_sets = []
        logging.debug("getting box coordinates")
        for b in self.bins:
            coords = []
            for box in b.boxes_packed:
                coords.append((box.centrefrom,box.centreto,box.rotateto))
            coord_sets.append(coords)
            logging.debug("box coordinates: {}".format(coord_sets))
        return coord_sets

    #score assumes that the boxdims include the offset
    def score(self, corner , w, l, bid):
        logging.debug("Calculating score for bin {}".format(bid))
        (blw,bll) = corner
        logging.debug("Bin Area: \n{}".format(self.bins[bid].area))
        total = 0
        #add up bottom width
        logging.debug("about to add up bottom width")
        if blw == 0:
            total += l
            logging.debug("blw is 0, added entire length")
        else:
            logging.debug("blw is not 0")
            for i in range(0,l):
                logging.debug("checking point ({},{})".format(blw-1,bll+i))
                if not self.bins[bid].area[blw-1][bll+i]:
                    logging.debug("adding 1")
                    total += 1
        #add up left length
        logging.debug("about to add up left length")
        if bll == 0:
            total += w
            logging.debug("bll is 0, added entire width")
        else:
            logging.debug("bll is not 0")
            for i in range(0,w):
                logging.debug("checking point ({},{})".format(blw+i,bll-1))
                if not self.bins[bid].area[blw+i][bll-1]:
                    logging.debug("adding 1")
                    total += 1
        #change (blw,bll) to top right corner
        blw += w; bll += l
        logging.debug("top right corner dims {},{}".format(blw,bll))
        #add up top width
        if blw == self.binSize[0]-1:
            total += l
            logging.debug("blw is binsize [{}], added entire length".format(blw))
        else:
            for i in range(0,l):
                logging.debug("checking point ({},{})".format(blw+1,bll-i))
                if not self.bins[bid].area[blw+1][bll-i]:
                    total += 1
        #add up right length
        if bll == self.binSize[1]-1:
            total += w
            logging.debug("bll is binsize [{}] added entire width".format(bll))
        else:
            for i in range(0,w):
                logging.debug("checking point ({},{})".format(blw-i,bll+1))
                if not self.bins[bid].area[blw-i][bll+1]:
                    total += 1
        #get float thing
        score = np.float32(total/(2*(w+l)))
        logging.debug("score: {}".format(score))
        return score

    def getPositions(self, w, l, bid):
        #list of tuples: positions by bottom left corner
        poslist = []
        logging.debug("whats in the box? {}".format(self.bins[bid].boxes_packed))
        if len(self.bins[bid].boxes_packed)>0:
            for box in self.bins[bid].boxes_packed:
                (cw,cl) = box.centreto
                bw = box.width+offset
                bl = box.length+offset
                topleft = (np.int8(cw-bw/2),np.int8(cl+bl/2))
                btmright = (np.int8(cw+bw/2),np.int8(cl-bl/2))
                corners = [topleft,btmright]
                logging.debug("corners possible: {}".format(corners))
                #add the corner if it is a suitable position
                for cor in corners:
                    if not self.binSize[0]-1 < cor[0]+w+offset and not self.binSize[1]-1 < cor[1]+l+offset:
                        if np.all(self.bins[bid].area[cor[0]:cor[0]+w+offset,cor[1]:cor[1]+l+offset]):
                            poslist.append(cor)

        else:
            poslist.append((0,0))
        logging.debug("poslist: {}".format(poslist))
        return poslist


    def compute_L(self):
        total_area = np.float32(0)
        bin_area = np.float32(self.binSize[0]*self.binSize[1])
        logging.debug("Type check total_area: {}, bin_area: {}".format(total_area.__class__, bin_area.__class__))
        for box in self.boxes:
            total_area += box.area
        L = np.int8(np.ceil(total_area/bin_area))
        logging.debug("Type check L: {}".format(L.__class__))
        return L

    def get_error(self):
        self.error.update({"Bins Used":len(self.bins)})
        self.calculate_waste()
        return self.error

    def calculate_waste(self):
        total_area_available = np.float32(0)
        total_area_packed = np.float32(0)
        for b in self.bins:
            total_area_available += b.length*b.width
            for pb in b.boxes_packed:
                total_area_packed += pb.area
        self.error.update({"Calculated Area Wastage":np.abs(total_area_available - total_area_packed)})
        tot = 0
        for b in self.bins:
            tot += np.sum(b.area)
        self.error.update({"Measured Area Wastage": tot})
