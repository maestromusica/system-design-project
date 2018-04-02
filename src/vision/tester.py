from Algorithm import StackingAlgorithm
from Parameters import test_boxes, test_box_set
from rectpack import newPacker, MaxRectsBl
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def run_test(which,bxs):
    sa = None
    if which == 'test' and bxs == 'set':
        sa = test_algo(test_box_set,(5,5))
    elif which == 'test' and bxs == 'test':
        sa = test_algo(test_boxes,(10,10))
    elif which == 'offline' and bxs == 'set':
        offline_test(test_box_set)
    elif which == 'offline' and bxs == 'test':
        offline_test(test_boxes)
        
    return sa


def test_algo(boxes, binsize, msa=None, bna=None, sta=None):
    maxsortalgs = msa or ['MaxRectsBaf', 'MaxRectsBl', 'MaxRectsBssf', 'MaxRectsBlsf', 'SkylineBl', 'SkylineBlWm', 'SkylineMwf', 'SkylineMwfl', 'SkylineMwfWm', 'SkylineMwflWm']
    binalgs = bna or ['NF','FF','BF']
    sortalgs = sta or ['WEIGHT','AREA','LENGTH','SSIDE','LSIDE','PERI','DIFF','RATIO','UNSORTED']

    sa = StackingAlgorithm(binsize,'BPRF')
    sa.pack(boxes)

    for alg in maxsortalgs:
        for b in binalgs:
            for s in sortalgs:
                sa.openNewPallet(alg+'_'+b,s)
                sa.pack(boxes)
                
            
    sa.displayStats()
    return sa
    
def offline_test(boxes):
    sa = newPacker(mode=1, bin_algo=3,pack_algo=MaxRectsBl,sort_algo='SORT_AREA', rotation=True)
    sa.add_bin(10,10,float('inf'))
    for box in boxes:
        sa.add_rect(box['length'],box['width'],str(box['centroid']))
        
    sa.pack()
    print(sa.rect_list())
    levels = []
    for i in range(len(sa)):
        levels.append({})
    for (b,x,y,w,l,rid) in sa.rect_list():
        levels[b][rid] = {'cor1':y*100,'cor2':x*100,'dim1':l*100,'dim2':w*100}
    print(levels)
    for l in levels:
        im = np.array(Image.open('Container2.png'), dtype=np.uint8)
        fig,ax = plt.subplots(1)
        ax.imshow(im)
        for k, b in l.items():
            rect = patches.Rectangle((b['cor1'],b['cor2']),b['dim1'],b['dim2'],linewidth=1,edgecolor='black')
            ax.add_patch(rect)
    print('about to show plot')
    plt.show()
    

