import paho.mqtt.client as mqtt
from Adapter import Adaptor
from Algorithm import StackingAlgorithm
from ..config.index import topics
from Vision import Vision
import cv2

grabVals = {'red':{'grab':0,'pickrelease':55,'droprelease':45},\
            'yellow':{'grab':0,'pickrelease':45,'droprelease':35},\
            'blue':{'grab':0,'pickrelease':45,'droprelease':45},\
            'green':{'grab':35,'pickrelease':65,'droprelease':45},\
            'purple':{'grab':0,'pickrelease':55,'droprelease':35}\
            }

class VisionAdaptor:
    def __init__(self,actionQueue):
        self.adaptor = Adaptor()
        self.vision = Vision()
        #self.stackAlg = StackingAlgorithm()
        self.actionQueue = actionQueue
        self.up = 80
        self.down = -195
        self.actionQueue.put(self.addResetAction('X'))
        self.actionQueue.put(self.addResetAction('Y'))
        #self.actionQueue.put(self.addResetAction('Z'))
        self.actionQueue.put(self.addZAction(self.up))
        self.actionQueue.put(self.addGrabAction(0))

    def addXAction(self,payload):
        return {
            "action": topics["EV3_MOVE_X"],
            "payload": payload
        }

    def addYAction(self,payload):
        return {
            "action": topics["EV3_MOVE_Y"],
            "payload": payload
        }

    def addZAction(self,payload):
        return {
            "action": topics["EV3_MOVE_Z"],
            "payload": payload
        }

    def addGrabAction(self,payload):
        return {
            "action": topics["EV3_MOVE_GRAB"],
            "payload": payload
        }

    def addReleaseAction(self,payload):
        return {
            "action": topics["EV3_MOVE_RELEASE"],
            "payload": payload
        }

    def addResetAction(self,axis):
        if axis == 'X':
            return {
            "action": topics["EV3_RESET_X"],
            "payload": None
            }
        elif axis == 'Y':
            return {
            "action": topics["EV3_RESET_Y"],
            "payload": None
            }
        '''
        elif axis == 'Z':
            return {
            "action": topics["EV3_RESET_Z"],
            "payload": None
            }
        '''

    def addRotateAction(self,payload):
        return{
            "action": topics["EV3_ROTATE"],
            "payload": payload
        }

    def grab(self,colour):
        self.actionQueue.put(self.addReleaseAction(grabVals[colour]['pickrelease']))
        self.actionQueue.put(self.addZAction(self.down))
        self.actionQueue.put(self.addGrabAction(grabVals[colour]['grab']))
        self.actionQueue.put(self.addZAction(self.up))
        return

    def drop(self,colour):
        self.actionQueue.put(self.addZAction(self.down))
        self.actionQueue.put(self.addReleaseAction(grabVals[colour]['droprelease']))
        self.actionQueue.put(self.addZAction(self.up))
        self.actionQueue.put(self.addGrabAction(0))
        return
    '''
    def gotoStart(self):
        self.controller.do_moveZ(400)
        self.controller.do_moveX(200)
        self.controller.do_moveY(200)
        return
    '''

    def createPickRoutine(self,box):
        #self.gotoStart()
        self.actionQueue.put(self.addZAction(self.up))
        print('Heading to package at : {}'.format(box.centrefrom))
        if box.rotateto == 90.00:
            self.actionQueue.put(self.addXAction(int(box.centrefrom[0])-75))
            self.actionQueue.put(self.addYAction(int(box.centrefrom[1])-20))
            self.actionQueue.put(self.addRotateAction(0))
        else:
            self.actionQueue.put(self.addXAction(int(box.centrefrom[0])-75))
            self.actionQueue.put(self.addYAction(int(box.centrefrom[1])-20))
            self.actionQueue.put(self.addRotateAction(-220))
        self.grab(box.colour)
        #self.actionQueue.put(self.addRotateAction(-220))
        #print('Package Recovered!')
        if True:
            self.actionQueue.put(self.addRotateAction(0))
            self.actionQueue.put(self.addXAction(int(box.centreto[1])))
            self.actionQueue.put(self.addYAction(int(box.centreto[0])))
        else:
            self.actionQueue.put(self.addRotateAction(0))
            self.actionQueue.put(self.addXAction(int(box.centreto[1])))
            self.actionQueue.put(self.addYAction(int(box.centreto[0])))
        self.drop(box.colour)
        print('Package Delivered!')

    def getFrame(self):
        self.image, self.boxes = self.vision.go()
        return self.image

    def execute(self, id=None):
        # Sending list of boxes to algorithm for stacking.
        sa = StackingAlgorithm((10,7), 'MaxRectsBl_BF', 'PERI')
        if id:
            sa.switchToPallet(id)
        id, bins = sa.pack(self.boxes)
        x = bins.copy()
        # Send these bins to Adaptor and transform pick and drop points.
        layers = self.adaptor.transform(x)
        for l in layers.keys():
            print("Creating pickup Routine for Layer: {}".format(l))
            for b in layers[l]:
                #self.createPickRoutine(b[0],b[1],b[2])
                #if b[4] == True:
                #    self.createPickRoutine(b[0],b[1],b[2],0.0)
                #else:
                    if b.newBox:
                        self.createPickRoutine(b)
                    b.centreto=b.centreto/100

        return id, bins

def main():
    va = VisionAdaptor()
    va.execute()
