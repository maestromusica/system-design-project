from os import path 
import _pickle as pkl

'''
workspace is hard coded here for now but possible to work on making a pickle file and a class where it finds the corners automatically to account for the camera moving about and stuff.
the mask values and camera parameters are read from pickle files. they should have the format like follows:

maskVals :: {'colourname':{'Erode':int,'Dilate':int,'OC':int,'High':array([r,g,b]),'Low':array([r,g,b]),'Blur':int,'Gamma':float,}}

camParams :: {'optmtx':[[float]],'mtx':[[float]],'distcoeffs':[]}
'''
class GlobalParams(object):

    def __init__(self):
        #should this be picklerick or demo?
        dir = path.dirname(path.abspath(__file__))
        self.mask = path.join(dir,'config/AllBoxesMask.pkl')
        self.cam = path.join(dir,'data/camera_intrinsic_params3.pkl')
        self.boardSize = (9,6)
        #coords go [col,row] ffs
        self.workspace = path.join(dir,'config/workspace_final_week.pkl')

    def findCorners(self,k):
        if k == 'TopLeft':
            return [0,0]
        if k == 'BottomLeft':
            return [0,800]
        if k == 'TopRight':
            return [475,0]

        if k == 'BottomRight':
            return [475,800]

    def getMaskVals(self,filename):
        if filename is None:
            filename = self.mask
        f = open(filename,'rb')
        maskVals = pkl.load(f)
        f.close()
        return maskVals

    def getCamParams(self, filename):
        if filename is None:
            filename = self.cam
        f = open(filename,'rb')
        optimal_matrix = pkl.load(f)
        matrix = pkl.load(f)
        dist = pkl.load(f)
        f.close()
        camParams = {'optmtx':optimal_matrix,'mtx':matrix,'distcoeffs':dist}
        return camParams

    
    def getWorkSpace(self,filename,workspace= None):
        if not filename:
            if workspace is None:
                filename = self.workspace
                print('reading from file: {}'.format(filename))                
                f = open(filename,'rb')
                workspace = pkl.load(f)
                f.close()
        for k in workspace.keys():
            workspace[k] = [workspace[k],self.findCorners(k)]
            print(workspace[k])
        return workspace

    def getBoardSize(self):
        return self.boardSize
    ''' some stuff to work on for extending maybe maybe not, we'll see
    def setMaskVals()

    def setCamParams()

    def setWorkSpace()
    '''
