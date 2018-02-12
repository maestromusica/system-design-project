import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('roi.png')
colors =['b','g','r']

for i,c in enumerate(colors):
    hist = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(hist,color=c)
    plt.xlim([0,256])
    
plt.show()
