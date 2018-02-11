#! /usr/bin/env python3
from queue import Queue
from message_types import Topics

class Controller:

    def __init__(self):
        self.boxes = None
        self.ev3ActionQueue = Queue()
        self.boxLocations = None

    def start(self):
        self.boxes = [
            {
                "length": 100,
                "width": 200,
                "height": 40,
                "x": 10,
                "y": 40
            },
            {
                "length": 40,
                "width": 20,
                "height": 90,
                "x": 10,
                "y": 90
            }
        ]
        self.getBoxArrangements()
        self.computeActionSequence()

    def nextAction(self):
        return self.ev3ActionQueue.get()

    def computeActionSequence(self):
        for box in self.boxes:
            self.ev3ActionQueue.put({
                "action": Topics.EV3_MOVE_X,
                "x": box["from"]["x"]
            })
            self.ev3ActionQueue.put({
                "action": Topics.EV3_MOVE_Y,
                "y": box["from"]["y"]
            })
            self.ev3ActionQueue.put({
                "action": Topics.EV3_MOVE_GRAB,
            })
            self.ev3ActionQueue.put({
                "action": Topics.EV3_MOVE_X,
                "x": box["to"]["x"]
            })
            self.ev3ActionQueue.put({
                "action": Topics.EV3_MOVE_Y,
                "y": box["to"]["y"]
            })
            self.ev3ActionQueue.put({
                "action": Topics.EV3_MOVE_RELEASE
            })

    def stop(self):
        # do nothing
        return

    def getBoxCoordinates(self):
        return self.boxes

    def getBoxArrangements(self):
        self.boxLocations = [
            {
                "to": {"x": 180, "y": 200},
                "from": {"x": 100, "y": 300}
            },
            {
                "to": {"x": 300, "y": 400},
                "from": {"x": 100, "y": 100}
            }
        ]

        for (i, box) in enumerate(self.boxes):
            box["from"] = self.boxLocations[i]["from"]
            box["to"] = self.boxLocations[i]["to"]

        return self.boxLocations
