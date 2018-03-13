from .Algorithm import StackingAlgorithm as a
import _pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

#testing the sorting part
boxes = [{'colour':'red','centroid':(1,1),'rotation':91.5,'width':4.1,'length':5.2}, \
{'colour':'red','centroid':(2,2),'rotation':91.5,'width':4.1,'length':5.2}, \
{'colour':'red','centroid':(3,3),'rotation':91.5,'width':5.7,'length':5.2}, \
{'colour':'red','centroid':(4,4),'rotation':91.5,'width':4.3,'length':5.6}, \
{'colour':'blue','centroid':(1,1),'rotation':5.6,'width':2.6,'length':4.3}, \
{'colour':'blue','centroid':(2,2),'rotation':5.6,'width':3.8,'length':3.2}, \
{'colour':'blue','centroid':(3,3),'rotation':5.6,'width':2.6,'length':3.9}, \
{'colour':'blue','centroid':(4,4),'rotation':5.6,'width':3.1,'length':2.8}, \
{'colour':'green','centroid':(1,1),'rotation':12.6,'width':2.7,'length':5.7}, \
{'colour':'green','centroid':(2,2),'rotation':12.6,'width':1.8,'length':4.3}, \
{'colour':'green','centroid':(3,3),'rotation':12.6,'width':6.4,'length':4.5}, \
{'colour':'yellow','centroid':(1,1),'rotation':12.6,'width':2.7,'length':5.7}, \
{'colour':'yellow','centroid':(2,2),'rotation':12.6,'width':2.8,'length':5.1}, \
{'colour':'yellow','centroid':(3,3),'rotation':12.6,'width':2.2,'length':4.5}, \
{'colour':'yellow','centroid':(4,4),'rotation':12.6,'width':5.8,'length':3.2}, \
{'colour':'yellow','centroid':(5,5),'rotation':12.6,'width':5.6,'length':5.2}, \
{'colour':'yellow','centroid':(6,6),'rotation':12.6,'width':4.7,'length':3.1}, \
{'colour':'purple','centroid':(1,1),'rotation':0,'width':2.5,'length':2.5}, \
{'colour':'purple','centroid':(2,2),'rotation':0,'width':2.5,'length':3.1}, \
{'colour':'purple','centroid':(3,3),'rotation':0,'width':1.4,'length':2.8}, \
{'colour':'purple','centroid':(4,4),'rotation':0,'width':1.9,'length':2.9}, \
{'colour':'purple','centroid':(5,5),'rotation':0,'width':2.1,'length':3.4}, \
{'colour':'purple','centroid':(6,6),'rotation':0,'width':2.1,'length':1.9}]
sa = a(boxes,(20,20),'BPRF')

##some sanity check output for sorting bit
print(":: Boxes ::")
for n, box in enumerate(sa.packer.boxes):
    print("  Box {}:: Colour: {}, Centre: {}, Width: {}, Length: {}".format(n, box.colour, box.centrefrom, box.width, box.length))
print(":: Packed Bins ::")
for n, sbin in enumerate(sa.packer.bins):
    print("  Boxes packed to Bin {}:".format(n))
    for m, box in enumerate(sbin.boxes_packed):
        print("    Box {}:: Colour: {}, Centre: {}) goes to Centre: {}, Width: {}, Length: {}".format(m, box.colour, box.centrefrom, box.centreto, box.width, box.length))
#testing getxy
print(":: Output ::")
print("  Get from xy to xy by layer: {}".format(sa.packer.get_xy()))


f = open(str(sa.timestamp)+'_error_log','rb')
error_mets = pkl.load(f)
f.close()

print(error_mets)

for sbin in sa.packer.bins:
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
        rect = patches.Rectangle(((box.centreto[0]-w/2)*100,(box.centreto[1]-l/2)*100),w*100,l*100,linewidth=1,edgecolor='black',facecolor=box.colour)
        ax.add_patch(rect)
    for i, w in enumerate(sbin.area):
        for j, l in enumerate(w):
            if l:
                rect = patches.Rectangle((i*100,j*100),100,100,linewidth=1,edgecolor='grey')
                ax.add_patch(rect)
    plt.show()
