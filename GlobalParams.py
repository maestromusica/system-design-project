import cPickle as pkl

'''
workspace is hard coded here for now but possible to work on making a pickle file and a class where it finds the corners automatically to account for the camera moving about and stuff.
the mask values and camera parameters are read from pickle files. they should have the format like follows:

maskVals :: {'colourname':{'Erode':int,'Dilate':int,'OC':int,'High':array([r,g,b]),'Low':array([r,g,b]),'Blur':int,'Gamma':float,}}

camParams :: {'optmtx':[[float]],'mtx':[[float]],'distcoeffs':[]}
'''
class GlobalParams(object):

    def __init__(self):
        #should this be picklerick or demo?
        self.mask = 'demo'
        self.cam = 'camera_intrinsic_params'
        self.boardSize = (9,6)
        #coords go [col,row] ffs
        self.workspace = {'topleft':([200,35],[0,0]),'bottomleft':([143,436],[0,500]),'topright':([416,38],[200,0]),'bottomright':([402,460],[200,500])}

    def getMaskVals(self,filename=None):
        if filename is not None:
            self.mask = filename
        f = open(self.mask)
        maskVals = pkl.load(f)
        f.close()
        return maskVals

    def getCamParams(self,filename=None):
        if filename is not None:
            self.cam = filename
        f = open(self.cam)
        camParams = pkl.load(f)
        f.close()
        return camParams

    def getWorkSpace(self,filename=None):
        if filename is not None:
            f = open(filename)
            self.workspace = pkl.load(f)
            f.close()
        return self.workspace

    def getBoardSize(self):
        return self.boardSize
    ''' some stuff to work on for extending maybe maybe not, we'll see
    def setMaskVals()

    def setCamParams()

    def setWorkSpace()
    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    '''
