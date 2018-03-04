class StackingAlgorithm:
    '''
    Creating a class StackingAlgorithm to find the endpoints of the boxes.
    For now the algorithm will Stack similar boxes together. In future, This class should
    be able to return a configuration of boxes to form a pallet that will be very space
    effecient.
    '''
    def __init__(self):
        # no state
        pass

    def getEndPoints(self,pl):
        plist= {}
        for (i,k) in enumerate(pl.keys()):
            if i == 0:
                x = 0
            elif i == 1:
                x = 250
            elif i == 2:
                x = 500
            elif i == 3:
                x = 750
            y = 0
            pickList = []
            for b in pl[k]:
                pickList.append([b,[x,y]])
                y += 280
            plist[i] = pickList
        return plist
