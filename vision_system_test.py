import cv2
import numpy as np
from src.utils.action_queue import ActionQueue
from src.vision.System import VisionAdaptor

visionAdaptor = VisionAdaptor(ActionQueue())
while True:
    frame = visionAdaptor.getFrame()
    cv2.imshow('frame',frame)
    k = cv2.waitKey(1)
    if k == 32:
        break
cv2.destroyAllWindows()
