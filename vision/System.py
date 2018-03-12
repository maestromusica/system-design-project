import paho.mqtt.client as mqtt
from Adapter import Adaptor
from Algorithm import StackingAlgorithm
from message_types import Topics
from Vision import Vision
import cv2

class VisionAdaptor:
    def __init__(self,actionQueue):
        self.adaptor = Adaptor()
        self.vision = Vision()
        #self.stackAlg = StackingAlgorithm()
        self.actionQueue = actionQueue
        self.actionQueue.put(self.addResetAction('X'))
        self.actionQueue.put(self.addResetAction('Y'))
        self.actionQueue.put(self.addResetAction('Z'))
        self.actionQueue.put(self.addZAction(500))
        self.actionQueue.put(self.addGrabAction())

    def addXAction(self,payload):
        return {
            "action": Topics.EV3_MOVE_X,
            "payload": payload
        }

    def addYAction(self,payload):
        return {
            "action": Topics.EV3_MOVE_Y,
            "payload": payload
        }

    def addZAction(self,payload):
        return {
            "action": Topics.EV3_MOVE_Z,
            "payload": payload
        }

    def addGrabAction(self):
        return {
            "action": Topics.EV3_MOVE_GRAB,
            "payload": 0
        }

    def addReleaseAction(self):
        return {
            "action": Topics.EV3_MOVE_RELEASE,
            "payload": 20
        }

    def addResetAction(self,axis):
        if axis == 'X':
            return {
            "action": Topics.EV3_RESET_X,
            "payload": None
            }
        elif axis == 'Y':
            return {
            "action": Topics.EV3_RESET_Y,
            "payload": None
            }
        elif axis == 'Z':
            return {
            "action": Topics.EV3_RESET_Z,
            "payload": None
            }
        
    def grab(self):
        self.actionQueue.put(self.addReleaseAction())
        self.actionQueue.put(self.addZAction(0))
        self.actionQueue.put(self.addGrabAction())
        self.actionQueue.put(self.addZAction(500))
        return

    def drop(self):
        self.actionQueue.put(self.addZAction(0))
        self.actionQueue.put(self.addReleaseAction())
        self.actionQueue.put(self.addZAction(500))
        self.actionQueue.put(self.addGrabAction())
        return
    '''
    def gotoStart(self):
        self.controller.do_moveZ(400)
        self.controller.do_moveX(200)
        self.controller.do_moveY(200)
        return
    '''
    
    def createPickRoutine(self,pickupPoint,endPoint):
        #self.gotoStart()
        print('Heading to package at : {}'.format(pickupPoint))
        self.actionQueue.put(self.addXAction(int(pickupPoint[0])))
        self.actionQueue.put(self.addYAction(int(pickupPoint[1])))
        self.grab()
        print('Package Recovered!')
        self.actionQueue.put(self.addXAction(int(endPoint[0])))
        self.actionQueue.put(self.addYAction(int(endPoint[1])))
        self.drop()
        print('Package Delivered!')

    def getFrame(self):
        image, _ = self.vision.go()
        return image
    
    def execute(self):
        while True:
            image, boxes = self.vision.go()
            cv2.imshow('output',image)
            k = cv2.waitKey(1)
            if k == ord('c'):
                # Sending list of boxes to algorithm for stacking.
                bins = StackingAlgorithm(boxes,(20,20),'BPOF').pack()

                # Send these bins to Adaptor and transform pick and drop points.
                layers = self.adaptor.transform(bins)
                print(layers)
                for l in layers.keys():
                    print("Creating pickup Routine for Layer: {}".format(l))
                    for b in layers[l]:
                        self.createPickRoutine(b[0],b[1])
                cv2.destroyAllWindows()
                return image

def main():
    va = VisionAdaptor()
    va.execute()

