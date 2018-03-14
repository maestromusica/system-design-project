import paho.mqtt.client as mqtt
from Adapter import Adaptor
from Algorithm import StackingAlgorithm
from ..config.index import topics
from Vision import Vision
import cv2

grabVals = {'red':{'grab':-140,'pickrelease':-100,'droprelease':-110},\
            'yellow':{'grab':-140,'pickrelease':-110,'droprelease':-120},\
            'blue':{'grab':-140,'pickrelease':-110,'droprelease':-110},\
            'green':{'grab':-120,'pickrelease':-90,'droprelease':-110},\
            'purple':{'grab':-140,'pickrelease':-110,'droprelease':-120}\
            }

class VisionAdaptor:
    def __init__(self,actionQueue):
        self.adaptor = Adaptor()
        self.vision = Vision()
        #self.stackAlg = StackingAlgorithm()
        self.actionQueue = actionQueue
        self.up = 350
        self.down = 120
        self.actionQueue.put(self.addResetAction('X'))
        self.actionQueue.put(self.addResetAction('Y'))
        #self.actionQueue.put(self.addResetAction('Z'))
        self.actionQueue.put(self.addZAction(self.up))
        self.actionQueue.put(self.addGrabAction(-140))

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
        self.actionQueue.put(self.addGrabAction(-140))
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
        print('Heading to package at : {}'.format(pickupPoint))
        if rotation == 90.00:
            self.actionQueue.put(self.addXAction(int(box.centrefrom[0])))
            self.actionQueue.put(self.addYAction(int(box.centrefrom[1])))
            self.actionQueue.put(self.addRotateAction(220))
        else:
            self.actionQueue.put(self.addXAction(int(box.centrefrom[0])))
            self.actionQueue.put(self.addYAction(int(pickupPoint[1])))
            self.actionQueue.put(self.addRotateAction(0))
        self.grab(b.colour)
        #self.actionQueue.put(self.addRotateAction(-220))
        #print('Package Recovered!')
        if endrotation == 90.0:
            self.actionQueue.put(self.addRotateAction(0))
            self.actionQueue.put(self.addXAction(int(b.centreto[0])))
            self.actionQueue.put(self.addYAction(int(b.centreto[1])))
        else:
            self.actionQueue.put(self.addRotateAction(220))
            self.actionQueue.put(self.addXAction(int(b.centreto[0])))
            self.actionQueue.put(self.addYAction(int(b.centreto[1])))
        self.drop(b.colour)
        print('Package Delivered!')

    def getFrame(self):
        self.image, self.boxes = self.vision.go()
        return self.image
    
    def execute(self):
        # Sending list of boxes to algorithm for stacking.
        bins = StackingAlgorithm(self.boxes,(10,7),'BPOF').pack()
        # Send these bins to Adaptor and transform pick and drop points.
        layers = self.adaptor.transform(bins)
        for l in layers.keys():
            print("Creating pickup Routine for Layer: {}".format(l))
            for b in layers[l]:
                #self.createPickRoutine(b[0],b[1],b[2])
                #if b[4] == True:
                #    self.createPickRoutine(b[0],b[1],b[2],0.0)
                #else:
                    self.createPickRoutine(b)
        return

def main():
    va = VisionAdaptor()
    va.execute()

