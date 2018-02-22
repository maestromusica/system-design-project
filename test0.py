import cv2
import numpy as np
import cPickle as pickle
import sys
import json
from base import BoxExtractor
import GlobalParams as gp
from Vision import Vision


class Adaptor(object):
    def __init__(self):
        self.vision = Vision()
        
    def do_stuff():
        while True:
           image, boxes = self.vision.go()

           print(boxes)

adaptor = Adaptor()
adaptor.do_stuff()
