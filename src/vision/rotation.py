from Gods import ImageProcessor
import cv2
import numpy as np
from GlobalParams import GlobalParams

cap = cv2.VideoCapture(1)
gp = GlobalParams()
process = ImageProcessor(gp.getCamParams(None),gp.getWorkSpace(None),gp.getMaskVals(None))

while True:
    _, frame = cap.read()
    bimg, boxes = process.process(cv2.flip(frame,1))
    cv2.imshow('bimg',bimg)
    if cv2.waitKey(10) == 32:
        break

cv2.destroyAllWindows()
