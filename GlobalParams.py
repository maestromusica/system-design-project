import cPickle as pkl

'''
workspace is hard coded here for now but possible to work on making a pickle file and a class where it finds the corners automatically to account for the camera moving about and stuff.
the mask values and camera parameters are read from pickle files. they should have the format like follows:

maskVals :: {'colourname':{'Erode':int,'Dilate':int,'H_min':int,'H_max':int,
             'S_min':int,'S_max':int,'V_min':int,'V_max':int,'blur':int}}

camParams :: {'optmtx':[[float]],'mtx':[[float]],'distcoeffs':[]}
'''

mask = 'picklerick.pkl'
cam = 'camera_intrinsic_params.pkl'
work = {'topleft':([200,20],[0,0]),'bottomleft':([420,30],[200,0]),'topright':([150,470],[0,500]),'topleft':([415,475],[200,500])}
    

def getMaskVals(filename):
    if filename is not None:
        maskVals = filename
    else:
        maskVals = mask
    f = open(maskVals)
    maskVals = pkl.load(f)
    f.close()
    return maskVals

def getCamParams(filename):
    if filename is not None:
        camParams = filename
    else:
        camParams = cam
    f = open(camParams)
    camParams = pkl.load(f)
    f.close()
    return camParams

def getWorkSpace(filename):
    if filename is not None:
        f = open(filename)
        workspace = pkl.load(f)
        f.close()
    else:
        workspace = work
    return workspace


''' some stuff to work on for extending maybe maybe not, we'll see
def setMaskVals()

def setCamParams()

def setWorkSpace()
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
'''
