import paho.mqtt.client as mqtt
from Adapter import Adaptor
from Algorithm import StackingAlgorithm
from ..config.index import topics
from Vision import Vision
import cv2

class VisionAdaptor:
    def __init__(self,actionQueue):
        self.adaptor = Adaptor()
        self.vision = Vision()
        #self.stackAlg = StackingAlgorithm()
        self.actionQueue = actionQueue
        self.up = 0
        self.down = -350
        #self.actionQueue.put(self.addResetAction('X'))
        #self.actionQueue.put(self.addResetAction('Y'))
        #self.actionQueue.put(self.addResetAction('Z'))
        #self.actionQueue.put(self.addZAction(350))
        #self.actionQueue.put(self.addGrabAction())

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

    def addGrabAction(self):
        return {
            "action": topics["EV3_MOVE_GRAB"],
            "payload": -10
        }

    def addReleaseAction(self):
        return {
            "action": topics["EV3_MOVE_RELEASE"],
            "payload": 50
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
        
    def grab(self):
        self.actionQueue.put(self.addReleaseAction())
        self.actionQueue.put(self.addZAction(self.down))
        self.actionQueue.put(self.addGrabAction())
        self.actionQueue.put(self.addZAction(self.up))
        return

    def drop(self):
        self.actionQueue.put(self.addZAction(self.down))
        self.actionQueue.put(self.addReleaseAction())
        self.actionQueue.put(self.addZAction(self.up))
        self.actionQueue.put(self.addGrabAction())
        return
    '''
    def gotoStart(self):
        self.controller.do_moveZ(400)
        self.controller.do_moveX(200)
        self.controller.do_moveY(200)
        return
    '''
    
    def createPickRoutine(self,pickupPoint,endPoint,rotation):
        #self.gotoStart()
        print('Heading to package at : {}'.format(pickupPoint))
        if rotation == 90.00:
            self.actionQueue.put(self.addXAction(int(pickupPoint[0])-100))
            self.actionQueue.put(self.addYAction(int(pickupPoint[1])))
            self.actionQueue.put(self.addRotateAction(0))
        else:
            self.actionQueue.put(self.addXAction(int(pickupPoint[0])-100))
            self.actionQueue.put(self.addYAction(int(pickupPoint[1])))
            self.actionQueue.put(self.addRotateAction(-220))
        self.grab()
        self.actionQueue.put(self.addRotateAction(-220))
        print('Package Recovered!')
        self.actionQueue.put(self.addXAction(int(endPoint[0])))
        self.actionQueue.put(self.addYAction(int(endPoint[1])))
        self.drop()
        print('Package Delivered!')

    def getFrame(self):
        self.image, self.boxes = self.vision.go()
        return self.image
    
    def execute(self):
        # Sending list of boxes to algorithm for stacking.
        #bins = StackingAlgorithm(self.boxes,(20,20),'BPOF').pack()
          
        # Send these bins to Adaptor and transform pick and drop points.
        layers = self.adaptor.transform(self.boxes)
        print(layers)
        for l in layers.keys():
            print("Creating pickup Routine for Layer: {}".format(l))
            for b in layers[l]:
                self.createPickRoutine(b[0],b[1],b[2])
        return

def main():
    va = VisionAdaptor()
    va.execute()

