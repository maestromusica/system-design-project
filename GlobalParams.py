import cPickle as pkl

'''
workspace is hard coded here for now but possible to work on making a pickle file and a class where it finds the corners automatically to account for the camera moving about and stuff.
the mask values and camera parameters are read from pickle files. they should have the format like follows:

maskVals :: {'colourname':{'Erode':int,'Dilate':int,'H_min':int,'H_max':int,
             'S_min':int,'S_max':int,'V_min':int,'V_max':int,'blur':int}}

camParams :: {'optmtx':[[float]],'mtx':[[float]],'distcoeffs':[]}
'''

mask = 'saturday.pkl'
cam = 'camera_intrinsic_params.pkl'
work = {'topleft':([200,20],[0,0]),'bottomleft':([420,30],[200,0]),'topright':([150,470],[0,500]),'bottomright':([415,475],[200,500])}

def findCorners(k):
    if k == 'TopLeft':
        return [0,0]
    if k == 'BottomLeft':
        return [0,850]
    if k == 'TopRight':
        return [400,0]
    if k == 'BottomRight':
        return [400,850]

def getMaskVals(filename):
    if filename is None:
        filename = mask
    f = open(filename)
    maskVals = pkl.load(f)
    f.close()
    return maskVals

def getCamParams(filename):
    if filename is None:
        filename = cam
    f = open(filename)
    optimal_matrix = pkl.load(f)
    matrix = pkl.load(f)
    dist = pkl.load(f)
    f.close()
    camParams = {'optmtx':optimal_matrix,'mtx':matrix,'distcoeffs':dist}
    return camParams

def getWorkSpace(filename):
    if filename is None:
        filename = 'workspace.pkl'
    f = open(filename)
    workspace = pkl.load(f)
    f.close()
    for k in workspace.keys():
        workspace[k] = [workspace[k],findCorners(k)]
        print(workspace[k])
    return workspace


''' some stuff to work on for extending maybe maybe not, we'll see
def setMaskVals()

def setCamParams()

def setWorkSpace()
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
'''
