import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

def max_area_contour(mask):
    _,contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    max_area = 150
    select = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            select.append(cnt)
    return select

def extractBoundingRect(mask):
    contours = max_area_contour(mask)
    dims = []    
    for cnt in contours:
        # finding enclosing rectangle
        x,y,w,h = cv2.boundingRect(cnt)
        dims.append((x,y,w,h))
    return dims

def extractMinAreaRect(mask):
    contours = max_area_contour(mask)
    boxes = []
    for cnt in contours:
    # finding minimum area rect
        rect = cv2.minAreaRect(cnt)
        w,h = np.array(rect[1])
        h += 5; w+=5;
        box = cv2.boxPoints((rect[0],(w,h),rect[2]))
        box = np.int0(box)
        boxes.append((box,rect))
    return boxes

def fit_ellipse(mask):
    contours = max_area_contour(mask)
    ellipses = []
    for cnt in contours:
        ellipses.append(cv2.fitEllipse(cnt))
    return ellipses

def getColorMasks(img):

    # Applying Blur:
    img_blur = img.copy()
    for _ in xrange(3): 
        img_blur = cv2.bilateralFilter(img_blur,9,75,75)

    # Converting to HSV for color filtering.
    hsv = cv2.cvtColor(img_blur,cv2.COLOR_BGR2HSV)

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

def arrangeCorners(corners):
    '''
    This function arranges the Corners in a clockwise fashion.
    This function is important for correct estimation of pose of the boxes.
    '''
    return sorted(corners, key= lambda x:(x[0],x[1]))

def findGoodFeaturesToTrack(img, box):
    centroid = (0,0)
    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    corners = cv2.goodFeaturesToTrack(gray,20,0.03,10)
    if corners is not None:
        corners = corners.flatten().reshape(-1,2)
    else:
        print "Nothing in Corners."
        return img, centroid

    # defining Termination Criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.01)
    try:
        corners = cv2.cornerSubPix(gray,corners,(5,5),(-1,-1),criteria)
    except Exception as err:
        print "SubPix Error again"
        return img, centre
    #print("debug corners before nearest: {}".format(corners))
    #print("debug box corners: {}".format(box))
    corners = findNearestPoints(box,corners)
    #print("debug corners after nearest: {}".format(corners))

    if len(corners) == 4:
        # rearranging Corners:
        corners = arrangeCorners(corners)

        centroid = np.sum(corners,axis=0)/4
        for i in corners:
            x,y = i.ravel()
            cv2.circle(img,(x,y),2,[255,0,0],-1)
        cv2.circle(img,tuple(centroid),2,[255,0,0],-1)
        #print("Centroid X-Coordinate: %.2f and Y-Coordinate: %.2f" % (centroid[0], centroid[1]))
        cv2.line(img,tuple(corners[0]),tuple(corners[3]),[255,255,0],1)
        cv2.line(img,tuple(corners[1]),tuple(corners[2]),[255,255,0],1)
    else:
        print("Not Enough Corners: {}".format(corners))
    return img, centroid

def findNearestPoints(box, corners):
    best_corners = box.copy()
    for i,b in enumerate(box):
        min_dist = 10000
        for j,c in enumerate(corners):
            d = np.linalg.norm(c-b)
            #print("box: {}, corner: {}, dist: {}, min dist: {}".format(i,j,d,min_dist))
            if d<min_dist:
                best_corners[i] = c
                min_dist = d
    return best_corners
    
def run(img):
    process(['ColorObjectTracker.py',img,'minRect'])
    
def process(argv):

    if len(argv) < 3 | len(argv) > 3:
        print 'Please input image and segmentation type.\n Usage: ColorObjectTracker.py image [minRect|boundRect|ellipse]'
        raise SystemExit

    file = argv[1]
    seg = argv[2]
    
    # readin image:
    img = cv2.imread(file)
    #cap = cv2.VideoCapture(0)

    #while True:
    #    ret, img = cap.read()
    ## Converting from BGR 2 RGB for output using matplotlib
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Getting masks for each color
    masks = getColorMasks(img)

    # Extracting objects from mask using seg style
    objects = []
    for i,m in enumerate(masks):
#        cv2.imshow('mask'+str(i),m)
        if seg == 'ellipse':
            obj = fit_ellipse(m)
            objects.append(obj)
        elif seg == 'boundRect':
            obj = extractBoundingRect(m)
            objects.append(obj)
        elif seg == 'minRect':
            obj = extractMinAreaRect(m)
            objects.append(obj)
            
    # defining variables for plots and labels
    red = [0,0,255]
    green = [0,255,0]
    blue = [255,0,0]
    yellow = [0,255,255]
    colors = [red,green,yellow,blue]
    names = ['red','green','yellow','blue']

    # Drawing objects on images:
    for i,obj in enumerate(objects):
        print('\nNumber of {} boxes : {}'.format(names[i],len(obj)))
    
        if seg == 'boundRect':
            for (x,y,w,h) in obj:
                roi = img[y-5:y+h+5,x-5:x+w+5]
                img[y-5:y+h+5,x-5:x+w+5] = findGoodFeaturesToTrack(roi)
                img = cv2.rectangle(img,(x-5,y-5),(x+w+5,y+h+5),colors[i],1)
                
        elif seg == 'minRect':
            for (box,rect) in obj:
                maxx, maxy = np.max(box, axis=0)
                minx, miny = np.min(box, axis=0)
                roi = img[miny:maxy,minx:maxx]
                img[miny:maxy,minx:maxx], centroid = findGoodFeaturesToTrack(roi,box-[minx,miny])
                centroid=np.array(centroid)
                centroid+=[minx,miny]
                img = cv2.drawContours(img,[box],0,colors[i],2)
                print("MinRect :: Centroid: {}, Width,Height: {}, Rotation Angle: {}".format(rect[0],rect[1],rect[2]))
                #print("Good Features :: Centroid: {}".format(centroid))
                #return rect, centroid #returning the rect features and good feature centroid for future use to send to ev3 or something
       
        elif seg == 'ellipse':
            for ellipse in obj:
                img = cv2.ellipse(img,ellipse,colors[i],2)
                
                

    cv2.imshow(file,img)
    cv2.waitKey(0)


if __name__ == '__main__':
    main(sys.argv)
