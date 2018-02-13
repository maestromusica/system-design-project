#! /usr/bin/env python3

from message_types import Topics
from action_queue import ActionQueue, ActionQueueLockedException

class Controller:

    def __init__(self):
        self.boxes = None
        self.actionQueue = None
        self.boxLocations = None
        self.pendingAction = False

    def start(self):
        self.boxes = None
        self.actionQueue = ActionQueue()
        self.boxLocations = None

        self.getVideoFeed()
        self.computeBoxArrangements()
        self.computeActionSequence()

    def getVideoFeed(self):
        """Calls the video feed which will return an array of boxes"""

        self.boxes = [{
            "length": 100,
            "width": 200,
            "height": 40,
            "x": 10,
            "y": 40 }, {
            "length": 40,
            "width": 20,
            "height": 90,
            "x": 10,
            "y": 90
        }]

    def nextAction(self):
        if self.actionQueue.empty():
            return None
        else:
            return self.actionQueue.get()

    def unlockQueue(self):
        self.actionQueue.unlock()
        self.pendingAction = False

    def lockQueue(self):
        self.actionQueue.lock()

    def computeActionSequence(self):
        for box in self.boxes:
            self.actionQueue.put({
                "action": Topics.EV3_MOVE_X,
                "payload": {"x": box["from"]["x"]}
            })
            self.actionQueue.put({
                "action": Topics.EV3_MOVE_Y,
                "payload": {"y": box["from"]["y"]}
            })
            self.actionQueue.put({
                "action": Topics.EV3_MOVE_GRAB,
                "payload": {}
            })
            self.actionQueue.put({
                "action": Topics.EV3_MOVE_X,
                "payload": {"x": box["to"]["x"]}
            })
            self.actionQueue.put({
                "action": Topics.EV3_MOVE_Y,
                "payload": {"y": box["to"]["y"]}
            })
            self.actionQueue.put({
                "action": Topics.EV3_MOVE_RELEASE,
                "payload": {}
            })

    def stop(self):
        # do nothing
        return

    def computeBoxArrangements(self):
        self.boxLocations = [{
            "to": {"x": 180, "y": 200},
            "from": {"x": 100, "y": 300}},{
            "to": {"x": 300, "y": 400},
            "from": {"x": 100, "y": 100}
        }]

        for (i, box) in enumerate(self.boxes):
            box["from"] = self.boxLocations[i]["from"]
            box["to"] = self.boxLocations[i]["to"]
