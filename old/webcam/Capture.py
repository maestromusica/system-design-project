import cv2
import numpy as np

# Creating Camera Object
cap =  cv2.VideoCapture(0)

# Creating a while loop for getting a feed
count = 0
while True:
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    k = cv2.waitKey(10)
    if k == ord('s'):
        cv2.imwrite('Images/chessboard'+str(count)+'.png',frame)
        count += 1
    if k == 32:
        break

cv2.destroyAllWindows()

    
