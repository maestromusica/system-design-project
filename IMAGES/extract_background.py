import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True: 
    ret, frame = cap.read()
    
    cv2.imshow('frame',frame)
    
    k = cv2.waitKey(5)
    if k == ord('s'):
        cv2.imwrite('background1.png',frame)
    elif k == 32:
        break

cv2.destroyAllWindows()
