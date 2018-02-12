import cv2
import numpy as np
import matplotlib.pyplot as plt

def max_area_contour(mask):
    _,contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    select = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            select = cnt
    return select

def extractBoundingRect(mask):
    cnt = max_area_contour(mask)
  
    # finding enclosing rectangle
    x,y,w,h = cv2.boundingRect(cnt)
    return (x,y,w,h)

def extractMinAreaRect(mask):
    cnt = max_area_contour(mask)
    
    # finding minimum area rect
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    return box

def fit_ellipse(mask):
    cnt = max_area_contour(mask)
    return cv2.fitEllipse(cnt)

def getColorMasks(img):

    # Applying Blur:
    img_blur = img.copy()
    for _ in xrange(3): 
        img_blur = cv2.bilateralFilter(img_blur,9,75,75)

    # Converting to HSV for color filtering.
    hsv = cv2.cvtColor(img_blur,cv2.COLOR_RGB2HSV)

    # Color_filtering for red:
    lower_red = np.array([0,100,100])
    higher_red = np.array([20,255,255])
    
    # Color_filtering for yellow
    lower_yellow = np.array([20,80,0])
    higher_yellow = np.array([40,255,255])
    
    #Color_filtering for blue
    lower_blue = np.array([100,80,0])
    higher_blue = np.array([120,255,255])

    # Color_filtering for green:
    lower_green = np.array([60,100,100])
    higher_green = np.array([80,255,255])

    lower = [lower_red,lower_green,lower_yellow,lower_blue]
    higher = [higher_red,higher_green,higher_yellow,higher_blue]
    masks = []
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    for l,h in zip(lower,higher):
        # obtaining mask
        mask = cv2.inRange(hsv,l,h)
    
        # applying closing operation
        for _ in xrange(3):
            mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)

        masks.append(mask)
    return masks


def main():
    
    file = '../IMAGES/object0.png'
    # readin image:
    img = cv2.imread(file)

    # Converting from BGR 2 RGB for output using matplotlib
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    masks = getColorMasks(img)

    '''
    # Using mask to obtain thresholded images
    images = []
    for m in masks:
        image = cv2.bitwise_and(img,img,mask=m)
        images.append(image)

    '''
    objects = []
    for m in masks:
	plt.figure()
	plt.imshow(m)
        obj = extractMinAreaRect(m)
        objects.append(obj)


    
    # displaying images
    #colors = ['red','green','yellow','blue']

    '''
    for i,img in enumerate(images):
        plot = '22' + str(i+1)
        plt.subplot(int(plot))
        plt.imshow(img)
        plt.title(colors[i])
        plt.xticks([])
        plt.yticks([])
    '''
    red = [255,0,0]
    green = [0,255,0]
    blue = [0,0,255]
    yellow = [255,255,0]

    colors = [red,green,yellow,blue]
    for i,box in enumerate(objects):
        #img = cv2.ellipse(img,box,colors[i],2)
        img = cv2.drawContours(img,[box],0,colors[i],2)
        print(box)
        #img =  cv2.rectangle(img,(x,y),(x+w,y+h),colors[i],2)

    plt.figure()
    plt.imshow(img)

    plt.show()

if __name__ == '__main__':
    main()
