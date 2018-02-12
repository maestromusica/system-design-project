import cv2
import numpy as np

file = '../IMAGES/objects1.jpg'

# reading file

img = cv2.imread(file)

# Scaling down image to reduce resolution.

for _ in xrange(2):
    img = cv2.pyrDown(img)

# Saving image as 'objects_reduced.jpg'

cv2.imwrite('../IMAGES/objects1.png',img)

