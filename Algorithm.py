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
        for k in pl.keys():
            if k == 'red':
                x = 0
            elif k == 'green':
                x = 180
            elif k == 'blue':
                x = 360
            elif k == 'yellow':
                x = 540
            y = 0
            pickList = []
            for b in pl[k]:
                pickList.append([b,[x,y]])
                y += 250
            pl[k] = pickList
        return pl
