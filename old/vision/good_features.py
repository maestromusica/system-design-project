import cv2
import numpy as np
import matplotlib.pyplot as plt

file = '../IMAGES/object0.png'

img = cv2.imread(file)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray,50,0.03,10)
corners = np.int0(corners)

for i in corners:
    x,y = i.ravel()
    cv2.circle(img,(x,y),3,255,-1)

cv2.imshow('corners',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
