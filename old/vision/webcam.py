import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    cv2.imshow('frame',frame)
    k = cv2.waitKey(1)
    if k == ord('c'):
        cv2.imwrite('webcam.png',frame)
    elif k == 32:
        break
cv2.destroyAllWindows()

    
        
