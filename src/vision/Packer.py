from Containers import Bin
import logging
import numpy as np
from rectpack import float2dec, newPacker, MaxRectsBaf, MaxRectsBl, MaxRectsBssf, MaxRectsBlsf, SkylineBl, SkylineBlWm, SkylineMwf, SkylineMwfl, SkylineMwfWm, SkylineMwflWm
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import uuid

class SimpleGreedy(object):

    def __init__(self, boxes, binSize):
        self.binSize = binSize
        self.error = {'Free Space':{0:0},'Bins Expected':0,'Density':{0:0},'Bins Used':0}
        self.bins = []


    def sort(self, boxes):

        boxes = sorted(boxes, reverse=True, key=lambda box: (box.length,box.width))


        #compute L, the number of expected bins
        L = self.compute_L([box.area for box in sorted_boxes])

        #create the bins to be packed into
        while L > 0:
            self.bins.append(Bin(self.binSize))
            L -= 1

        self.error.update({"Bins Expected":len(self.bins)})

        for box in sorted_boxes:
            b = 0
            while not box.packed:
                try:
                    self.pack(self.bins[b],box)
                    b += 1
                except IndexError:
                    self.bins.append(Bin(self.binSize))

        bns = len(self.bins)
        rtl = False

        for box in sorted_boxes:
            b = 0
            while not box.packed:
                try:
                    self.pack(self.bins[b],box)
                    b += 1
                except IndexError:
                    self.bins.append(Bin(self.binSize))



    def compute_L(self, boxes):
        total_area = sum(boxes)
        bin_area = self.binSize[0]*self.binSize[1]
        for b in self.bins:
                total_area -= b.freeArea
        L = np.int8(np.ceil(total_area/bin_area))
        return L


    def pack(self, con, box, rtl):

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
                    if y.width + b_w > 2*( np.abs( c0 - c_w) + 0.001 ) and y.length + b_l > 2*( np.abs( c1 - c_l) + 0.001 ) :
                        overlap = True
                        break
                if inside and not overlap:
                    #print(con.ws)
                    box.centreto = np.array(([ c_w ,c_l]))
                    con.ws.append(w + b_w)
                    con.ls.append(l + b_l)
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
        bin_area = self.binSize[0]*self.binSize[1]
        for i, b in enumerate(self.bins):
            self.error['Free Space'][i] = b.freeArea
            self.error['Density'][i] = sum([box.area for box in b.boxes_packed])/bin_area

        return self.error




class BPRF(object):

    def __init__(self, binSize, sort_t):
        self.binSize = binSize
        self.bins = []
        self.error = {'Free Space':{0:0},'Bins Expected':0,'Density':{0:0},'Bins Used':0}
        self.sort_t = sort_t or 'AREA'


    def sort(self, boxes):
        #Sort the Boxes to be packed by nonincreasing area
        sorted_boxes = sorted(boxes, reverse=True, key=lambda box: (box.area,max(box.width,box.length)))

        #compute L, the number of expected bins
        L = self.compute_L([box.area for box in sorted_boxes])
        #create the bins to be packed into
        while L > 0:
            self.bins.append(Bin(self.binSize))
            L -= 1

        self.error.update({"Bins Expected":len(self.bins)})

        for box in sorted_boxes:
            b = 0
            while not box.packed:
                try:
                    self.pack(self.bins[b],box)
                    b += 1
                except IndexError:
                    self.bins.append(Bin(self.binSize))

    def compute_L(self, boxes):
        total_area = sum(boxes)
        bin_area = self.binSize[0]*self.binSize[1]
        for b in self.bins:
                total_area -= b.freeArea
        L = np.int8(np.ceil(total_area/bin_area))
        return L

    def pack(self, con, box):

        smax = -1
        rotate = False
        cto_w = 0
        cto_l = 0
        w_new = 0
        l_new = 0

        for w in con.ws:
            for l in con.ls:
                x = [w,l]
                b_w = box.width
                b_l = box.length
                ## inside bin and bot overlap
                inside = con.inside(box,x)
                inside_R = con.inside_R(box,x)
                score = 0
                score_R = 0
                overlap = False
                c_w = w + b_w/2
                c_l = l + b_l/2
                con_w = con.width
                con_l = con.length
                overlap_R = False
                c_w_R = w + b_l/2
                c_l_R = l + b_w/2

                for y in con.boxes_packed :
                    c0 = y.centreto[0]
                    c1 = y.centreto[1]

                    if y.width + b_w > 2*( np.abs( c0 - c_w) + 0.001 ) and y.length + b_l > 2*( np.abs( c1 - c_l) + 0.001 ) :
                        overlap = True
                        break

                    if np.abs( y.width + b_w - 2*( np.abs( c0 - c_w) ) ) < 0.01:
                        score = score + np.maximum( 0 , ( (y.length + b_l)*0.5 - np.abs( c1 - c_l) ) )
                    if np.abs( y.length + b_l - 2*( np.abs( c1 - c_l) ) ) < 0.01:
                        score = score + np.maximum( 0 , (y.width + b_w)*0.5 - np.abs( c0 - c_w) )

                if l == 0 :
                    score = score + b_w
                if w == 0 :
                    score = score + b_l
                if np.abs(con_w - w - b_w ) < 0.1:
                    score = score + b_l
                if np.abs(con_l - l - b_l ) < 0.1:
                    score = score + b_w

                if l == 0 :
                    score_R = score_R + b_l
                if w == 0 :
                    score_R = score_R + b_w
                if np.abs(con_w - w - b_l ) < 0.1:
                    score_R = score_R + b_l
                if np.abs(con_l - l - b_w ) < 0.1:
                    score_R = score_R + b_w

                for y in con.boxes_packed :
                    c0 = y.centreto[0]
                    c1 = y.centreto[1]
                    if y.width + b_l > 2*( np.abs( c0 - c_w_R) + 0.001 ) and y.length + b_w > 2*( np.abs( c1 - c_l_R) + 0.001 ) :
                        overlap_R = True
                        break
                    if np.abs( y.width + b_w - 2*( np.abs( c0 - c_w_R) ) ) < 0.01:
                        score_R = score_R + np.maximum( 0 , ( (y.length + b_w)*0.5 - np.abs( c1 - c_l_R) ) )
                    if np.abs( y.length + b_l - 2*( np.abs( c1 - c_l_R) ) ) < 0.01:
                        score_R = score_R + np.maximum( 0 , (y.width + b_l)*0.5 - np.abs( c0 - c_w_R) )



                if inside and not overlap:
                    box.packed = True
                    if score > smax :
                        smax = score
                        rotate = False
                        cto_w = c_w
                        cto_l = c_l
                        w_new = w + b_w
                        l_new = l + b_l



                elif inside_R and not overlap_R:
                    box.packed = True
                    if score_R > smax :
                        smax = score_R
                        rotate = True
                        cto_w = c_w_R
                        cto_l = c_l_R
                        w_new = w + b_l
                        l_new = l + b_w



        if box.packed:
            if rotate:
                box.rotateto = 90.00
                box.vec = np.array([box.length,box.width])
            else: box.rotateto = 0.00
            box.centreto = np.array(([ cto_w, cto_l ]))
            con.boxes_packed.append(box)
            con.freeArea -= box.area
            con.ws.append( w_new )
            con.ls.append( l_new )
            con.ws.sort()
            con.ls.sort()
        #print(box.packed)
        #print(con.ls)
        #print(smax)
        return box.packed


    def get_error(self):
        self.error.update({"Bins Used":len(self.bins)})
        bin_area = self.binSize[0]*self.binSize[1]
        for i, b in enumerate(self.bins):
            self.error['Free Space'][i] = b.freeArea
            self.error['Density'][i] = sum([box.area for box in b.boxes_packed])/bin_area

        return self.error



class RectPacker(object):
    def __init__(self, binSize, ba, pa, st):
        self.binSize = binSize
        self.bins = []
        self.error = {'Free Space':{0:0},'Bins Expected':0,'Density':{0:0},'Bins Used':0}
        #to use GB made mode 1, but it moves boxes around on the pallet
        self.packer = newPacker(mode = 0,bin_algo = ba ,pack_algo=pa, rotation=True)
        self.packer.add_bin(self.binSize[0],self.binSize[1],float('inf'))
        self.sort_t = st or 'WEIGHT'


    def boxSort(self, boxes):
        if self.sort_t == 'WEIGHT':
            sorted_boxes = sorted(boxes, reverse=True, key=lambda box: box.weight) #sort by weight
        elif self.sort_t =='AREA':
            sorted_boxes = sorted(boxes, reverse=True, key=lambda box: box.area) #sort by area
        elif self.sort_t == 'LENGTH':
            sorted_boxes = sorted(boxes, reverse=True, key=lambda box: box.length) #sort by length
        elif self.sort_t == 'SSIDE':
            sorted_boxes = sorted(boxes, reverse=True, key=lambda box: (min(box.width,box.length), max(box.width,box.length))) #sort by short side
        elif self.sort_t == 'LSIDE':
            sorted_boxes = sorted(boxes, reverse=True, key=lambda box: (max(box.width,box.length), min(box.width,box.length))) #sort by long side
        elif self.sort_t == 'PERI':
            sorted_boxes = sorted(boxes, reverse=True, key=lambda box: box.length+box.width) # Sort by perimeter
        elif self.sort_t == 'DIFF':
            sorted_boxes = sorted(boxes, reverse=True, key=lambda box: abs(box.length-box.width)) # Sort by Diff
        elif self.sort_t == 'RATIO':
            sorted_boxes = sorted(boxes, reverse=True, key=lambda box: box.length/box.width) # Sort by side ratio
        else:
            sorted_boxes = boxes
        return sorted_boxes

    def sort(self, boxes):

        self.error['Bins Expected'] += self.compute_L([box.area for box in boxes])

        sorted_boxes = self.boxSort(boxes)

        packed_boxes = {}
        for box in sorted_boxes:
            rid = uuid.uuid4().hex
            self.packer.add_rect(box.width,box.length,rid)
            box.newBox = True
            packed_boxes[rid] = box
        #uncomment to use offline packing
        #self.packer.pack()

        L = len(self.packer) - len(self.bins)
        while L > 0:
            self.bins.append(Bin(self.binSize))
            L -=1

        for (b,x,y,w,l,rid) in self.packer.rect_list():
            try:
                box = packed_boxes[rid]
                self.pack(box,self.bins[b],x,y,w,l)
            except KeyError:
                #box already packed
                pass



    def showRectList(self):
        levels = []
        for i in range(len(self.packer)):
            levels.append({})
        for (b,x,y,w,l,rid) in self.packer.rect_list():
            levels[b][str(x)+str(y)+rid] = {'cor1':y*100,'cor2':x*100,'dim1':l*100,'dim2':w*100}
        for l in levels:
            im = np.array(Image.open('Container2.png'), dtype=np.uint8)
            fig,ax = plt.subplots(1)
            ax.imshow(im)
            for k, b in l.items():
                rect = patches.Rectangle((b['cor1'],b['cor2']),b['dim1'],b['dim2'],linewidth=1,edgecolor='black')
                ax.add_patch(rect)
        plt.show()

    def pack(self,box,b,x,y,w,l):
        #box object, bin object, x and y of bl corner, w and l of packed rectangle (possibly rotated)
        corner = np.array([x,y])

        if box.width == w and box.length == l:
            box.rotateto = 0.00
        elif box.width == l and box.length == w:
            box.rotateto = 90.00
            box.vec = np.array([box.length,box.width])
        else:
            print('LENGTH WIDTH MISTAKE')
            print(box.centrefrom,box.width,w,box.length,l,box.colour)

        box.centreto = corner+box.vec/2
        box.packed = True

        b.boxes_packed.append(box)
        b.freeArea -= box.area


    def compute_L(self, boxes):
        total_area = sum(boxes)
        bin_area = self.binSize[0]*self.binSize[1]
        for b in self.bins:
                total_area -= b.freeArea
        L = np.int8(np.ceil(total_area/bin_area))
        return L

    #maybe need to mod this
    def get_error(self):
        self.error.update({"Bins Used":len(self.bins)})
        bin_area = self.binSize[0]*self.binSize[1]
        for i, b in enumerate(self.bins):
            self.error['Free Space'][i] = b.freeArea
            self.error['Density'][i] = sum([box.area for box in b.boxes_packed])/bin_area

        return self.error



class MaxRectsBaf_NF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 0, MaxRectsBaf, sort_t)


class MaxRectsBaf_FF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 1, MaxRectsBaf, sort_t)


class MaxRectsBaf_BF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 2, MaxRectsBaf, sort_t)

class MaxRectsBaf_GB(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 3, MaxRectsBaf, sort_t)

class MaxRectsBl_NF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 0, MaxRectsBl, sort_t)


class MaxRectsBl_FF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 1, MaxRectsBl, sort_t)


class MaxRectsBl_BF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 2, MaxRectsBl, sort_t)

class MaxRectsBl_GB(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 3, MaxRectsBl, sort_t)


class MaxRectsBssf_NF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 0, MaxRectsBssf, sort_t)


class MaxRectsBssf_FF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 1, MaxRectsBssf, sort_t)


class MaxRectsBssf_BF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 2, MaxRectsBssf, sort_t)

class MaxRectsBssf_GB(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 3, MaxRectsBssf, sort_t)


class MaxRectsBlsf_NF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 0, MaxRectsBlsf, sort_t)


class MaxRectsBlsf_FF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 1, MaxRectsBlsf, sort_t)


class MaxRectsBlsf_BF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 2, MaxRectsBlsf, sort_t)

class MaxRectsBlsf_GB(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 3, MaxRectsBlsf, sort_t)


class SkylineBlWm_BF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 2, SkylineBlWm, sort_t)

class SkylineBl_BF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 2, SkylineBl, sort_t)

class SkylineMwf_BF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 2, SkylineMwf, sort_t)

class SkylineMwfl_BF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 2, SkylineMwfl, sort_t)

class SkylineMwflWm_BF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 2, SkylineMwflWm, sort_t)

class SkylineMwfWm_BF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 2, SkylineMwfWm, sort_t)

class SkylineBlWm_NF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 0, SkylineBlWm, sort_t)

class SkylineBl_NF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 0, SkylineBl, sort_t)

class SkylineMwf_NF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 0, SkylineMwf, sort_t)

class SkylineMwfl_NF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 0, SkylineMwfl, sort_t)

class SkylineMwflWm_NF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 0, SkylineMwflWm, sort_t)

class SkylineMwfWm_NF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 0, SkylineMwfWm, sort_t)

class SkylineBlWm_FF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 1, SkylineBlWm, sort_t)

class SkylineBl_FF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 1, SkylineBl, sort_t)

class SkylineMwf_FF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 1, SkylineMwf, sort_t)

class SkylineMwfl_FF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 1, SkylineMwfl, sort_t)

class SkylineMwflWm_FF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 1, SkylineMwflWm, sort_t)

class SkylineMwfWm_FF(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 1, SkylineMwfWm, sort_t)


class SkylineBlWm_GB(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 3, SkylineBlWm, sort_t)

class SkylineBl_GB(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 3, SkylineBl, sort_t)

class SkylineMwf_GB(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 3, SkylineMwf, sort_t)

class SkylineMwfl_GB(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 3, SkylineMwfl, sort_t)

class SkylineMwflWm_GB(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 3, SkylineMwflWm, sort_t)

class SkylineMwfWm_GB(RectPacker):
    def __init__(self, binSize, sort_t=None):
        super().__init__(binSize, 3, SkylineMwfWm, sort_t)
