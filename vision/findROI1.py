import cv2
import numpy as np
import matplotlib.pyplot as plt

# Reading File
img = cv2.imread('objects_reduced.jpg')

# blurring image
img_blur = cv2.bilateralFilter(img,9,75,75)

# Converting to HSV
hsv = cv2.cvtColor(img_blur,cv2.COLOR_BGR2HSV)

# ColorFiltering to focus on white
lower = np.array([22,0,0])
higher = np.array([42,255,255])

# creating mask
mask = cv2.inRange(hsv,lower,higher)

# applying morphological close
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
mask_closed = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)

# bitwise_and
masked_image = cv2.bitwise_and(img,img,mask=mask_closed)

# finding biggest contour
_,contours,_ = cv2.findContours(mask_closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

max_area = 0
select = None
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > max_area:
        max_area = area
    select = cnt

# Drawing Contour
#cv2.drawContours(masked_image,[select],0,[255,255,255],3)

# finding Enclosing Rectangle
rect = cv2.minAreaRect(select)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(masked_image,[box],0,(0,0,255),2)


# applying perspective transform
points = np.array([[0,373],[0,0],[267,0],[267,373]],np.float32)
M = cv2.getPerspectiveTransform(np.float32(box),points)
dst = cv2.warpPerspective(img,M,(267,373))

plt.subplot(221)
plt.imshow(img), plt.title('original')
plt.subplot(222)
plt.imshow(mask_closed), plt.title('mask')
plt.subplot(223)
plt.imshow(masked_image),plt.title('masked_image')
plt.subplot(224)
plt.imshow(dst), plt.title('perpective_changed')

print('Saving file to : roi.png')
cv2.imwrite('roi.png',dst)

plt.show()

