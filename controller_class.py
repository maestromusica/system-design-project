#! /usr/bin/env python3
class Controller:

    def __init__(self):
        self.boxes = None
        self.ev3ActionQueue = None
        self.boxLocations = None

    def start(self):
        self.getBoxCoordinates()
        self.getBoxArrangements()

    def stop(self):
        # do nothing
        return 

    def getBoxCoordinates(self):
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
            },
            {
                "length": 10,
                "width": 40,
                "height": 500,
                "x": 10,
                "y": 50
            }
        ]
        return self.boxes

    def getBoxArrangements(self):
        self.boxLocations = [
            {
                "x": 180,
                "y": 200
            },
            {
                "x": 300,
                "y": 400
            },
            {
                "x": 500,
                "y": 300
            }
        ]
        return self.boxLocations
