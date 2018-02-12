import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('roi.png')

Z = np.float32(img.reshape((-1,3)))


criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,10,1.0)

K = 10

ret, label, center = cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))

plt.imshow(res2)
plt.show()
    
