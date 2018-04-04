from Algorithm import StackingAlgorithm
from Parameters import test_boxes, test_box_set
from rectpack import newPacker, MaxRectsBl
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from random import randint

def run_test(which,bxs=None):
    sa = None
    if which == 'test' and bxs == 'set':
        sa = test_algo(test_box_set,(5,5))
    elif which == 'test' and bxs == 'test':
        sa = test_algo(test_boxes,(10,10))
    elif which == 'offline' and bxs == 'set':
        offline_test(test_box_set)
    elif which == 'offline' and bxs == 'test':
        offline_test(test_boxes)
    elif which == 'gen':
        bxs = generate_boxes()
        sa = test_algo(bxs,(12,12))
    return sa


def test_algo(boxes, binsize, msa=None, bna=None, sta=None):
    maxsortalgs = msa or ['MaxRectsBaf', 'MaxRectsBl', 'MaxRectsBssf', 'MaxRectsBlsf', 'SkylineBl', 'SkylineBlWm', 'SkylineMwf', 'SkylineMwfl', 'SkylineMwfWm', 'SkylineMwflWm']
    binalgs = bna or ['NF','FF','BF']
    sortalgs = sta or ['WEIGHT','AREA','LENGTH','SSIDE','LSIDE','PERI','DIFF','RATIO','UNSORTED']
    print('Test Packing {} Boxes into {}x{} Pallets'.format(len(boxes),binsize[0],binsize[1]))
    sa = StackingAlgorithm(binsize,'BPRF')
    sa.pack(boxes)
    
    for alg in maxsortalgs:
        for b in binalgs:
            for s in sortalgs:
                sa.openNewPallet(alg+'_'+b,s)
                sa.pack(boxes)
                
            
    analyseStats(sa.stats)
    sa.saveStats()
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
    
def generate_boxes():
    #colour, centroid, rotation, length, width
    cls = ['red','green','blue','purple','yellow']
    centroid = np.array([0,0])
    rot = [90.00,0.00]
    boxes = []
    for i in range(randint(10,100)):
        boxes.append({'colour':cls[randint(0,4)],'rotation':rot[randint(0,1)],'centroid':centroid})
    return boxes
    

def analyseStats(stats):
    #density, [[alg,sort,pallet,level]]
    best_density = (0.0,[])
    best_runtime = (float('inf'),'None', (0,0))
    for k, v in stats.items():
        if len(k)<32:
            runtime = sum([t for (t,_) in v['Runtime for Boxes']])
            total_boxes = sum([b for (_,b) in v['Runtime for Boxes']])
            if runtime/len(v['Runtime for Boxes']) < best_runtime[0]:
                best_runtime = (runtime/len(v['Runtime for Boxes']),k, runtime, total_boxes)
        if len(k) == 32:
            for i in range(v['Bins Used']):
                if v['Density'][i] > best_density[0]:
                    best_density = (v['Density'][i], [(v['Algorithm'],v['Box Sort Method'],k,i)])
                elif v['Density'][i] == best_density[0]:
                    best_density[1].append((v['Algorithm'],v['Box Sort Method'],k,i))
            
            
    print('Best Average Runtime: {}s by {} with a total of {}s over {} boxes'.format(best_runtime[0],best_runtime[1],best_runtime[2], best_runtime[3]))
    print('Best Density:')
    
    pallets_at_max = [bd[2] for bd in best_density[1] if bd[3] == 0]
    i = 1
    final_best_pallets = set([])
    while len(pallets_at_max)>0:
        #print('going over level {}'.format(i))
        for pid in pallets_at_max.copy():
            if i >= stats[pid]['Bins Used']:
                final_best_pallets.update({pid})
                #print('updated final best pallets with {}'.format(pid))
                pallets_at_max.remove(pid)
                #print('removed {} from pallets at max'.format(pid))
            #print('final best pallets after additions: {}'.format(final_best_pallets))
            #print('pallets at max after removals:')
            #print('   {} bins in {}'.format(stats[pid]['Bins Used'],pid))
            #print('   {} densities'.format(stats[pid]['Density']))
        if len(pallets_at_max)>0:
            max_density = max([stats[pidm]['Density'][i] for pidm in pallets_at_max])
            #print('max density: {}'.format(max_density))
            pallets_at_max = [pid for pid in pallets_at_max if stats[pid]['Density'][i] == max_density]
            #print('new pallets at max {}'.format(len(pallets_at_max)))
        i += 1    
    displayStats(stats, algs=[stats[pid]['Algorithm'] for pid in final_best_pallets], pals=final_best_pallets)
    
def displayStats(stats, algs=[], pals=[]):
    
    for k, v in stats.items():
        if len(k)<32 and k in algs:
            print('Algorithm: '+k)
            runtime = sum([t for (t,_) in v['Runtime for Boxes']])
            total_boxes = sum([b for (_,b) in v['Runtime for Boxes']])
            print('    Total Runtime: {}s over {} boxes into {} pallets'.format(runtime,total_boxes,len(v['Runtime for Boxes'])))
            print('    Average Time Per Pallet: {}s'.format(runtime/len(v['Runtime for Boxes'])))
        elif len(k) == 32 and k in pals:
            print('Pallet {}: Packed by {} and sorted by {}'.format(k,v['Algorithm'],v['Box Sort Method']))
            b = v['Boxes Packed']
            print('    {} boxes packed onto {} levels'.format(b,v['Bins Used']))
            print('    {} levels expected'.format(v['Bins Expected']))
            
            for i in range(v['Bins Used']):
                print('    Level {}:'.format(i))
                print('        Density: {}% packed'.format(v['Density'][i]))
                print('        Free Space: {} sq units'.format(v['Free Space'][i]))
                
                

    
