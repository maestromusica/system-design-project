import cv2
import Calibrator
import numpy as np
import matplotlib.pyplot as plt
import sys
import cPickle as pickle

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

def getColorMasks(img,pkl):

    # getting values from file instead
    f = open(str(pkl))
    params = pickle.load(f)
    f.close()
    masks = []
    kernel = np.ones((5,5))
    
    ##red green yellow blue, prolly need to fix that.
    for colour in ['red','green','yellow','blue']:
        values = params[colour]
        erode = values['Erode']
        dilate = values['Dilate']
        low = np.array([values['H_min'],values['S_min'],values['V_min']])
        high = np.array([values['H_max'],values['S_max'],values['V_max']])

        blur = values['blur']

        # Applying Blur:
        img_blur = img.copy()
        for _ in xrange(5): 
            img_blur = cv2.bilateralFilter(img_blur,9,75,75)

        # Converting to HSV for color filtering.
        hsv = cv2.cvtColor(img_blur,cv2.COLOR_BGR2HSV)

        #mask is in range
        mask = cv2.inRange(hsv,low,high)
        #erode and dilate
        mask = Calibrator.open_close(mask,kernel,params)
        #append to masks
        masks.append(mask)
       
    return masks

def arrangeCorners(corners):
    '''
    This function arranges the Corners in a clockwise fashion.
    This function is important for correct estimation of pose of the boxes.
    '''
    return sorted(corners, key= lambda x:(x[0],x[1]))

def findGoodFeaturesToTrack(img,box):
    centroid = (0,0)
    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    corners = cv2.goodFeaturesToTrack(gray,20,0.03,10)
    if corners is not None:
        corners = corners.flatten().reshape(-1,2)
    else:
        print "Nothing in Corners."
        return corners, centroid

    # defining Termination Criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.01)
    try:
        corners = cv2.cornerSubPix(gray,corners,(5,5),(-1,-1),criteria)
    except Exception as err:
        print "SubPix Error again"
        return corners, centroid
    corners = findNearestPoints(box,corners)
    
    if len(corners) == 4:
        # rearranging Corners:
        corners = arrangeCorners(corners)

        centroid = np.sum(corners,axis=0)/4
    else:
        print("Not Enough Corners: {}".format(corners))
    return corners, centroid

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

def process_frame(img, pkl,seg='minRect'):

    # Getting masks for each color
    masks = getColorMasks(img,pkl)

    # Extracting objects from mask using seg style
    objects = []
    for i,m in enumerate(masks):
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
        print('Number of {} boxes : {}'.format(names[i],len(obj)))
    
        if seg == 'boundRect':
            for (x,y,w,h) in obj:
                roi = img[y-5:y+h+5,x-5:x+w+5]
                img[y-5:y+h+5,x-5:x+w+5] = findGoodFeaturesToTrack(roi)
                img = cv2.rectangle(img,(x-5,y-5),(x+w+5,y+h+5),colors[i],1)
                
        elif seg == 'minRect':
            for (box,rect) in (obj):
                #maxx, maxy = np.max(box, axis=0)
                #minx, miny = np.min(box, axis=0)
                roi = cv2.bitwise_and(img,img,mask = masks[i])
                cv2.imshow(names[i],roi)
                cv2.waitKey(0)
                corners , centroid = findGoodFeaturesToTrack(roi,box)
                centroid=np.array(centroid)
                for z in corners:
                    x,y = z.ravel()
                    cv2.circle(img,(x,y),3,[0,0,255],-1)
                    cv2.circle(img,tuple(centroid),2,[0,0,255],-1)
                    #print("Centroid X-Coordinate: %.2f and Y-Coordinate: %.2f" % (centroid[0], centroid[1]))
                    cv2.line(img,tuple(corners[0]),tuple(corners[3]),[0,0,255],1)
                    cv2.line(img,tuple(corners[1]),tuple(corners[2]),[0,0,255],1)

                img = cv2.drawContours(img,[box],0,colors[i],2)
                print("MinRect :: Centroid: {}, Width,Height: {}, Rotation Angle: {}".format(rect[0],rect[1],rect[2]))
                print("Good Features :: Cenroid: {}".format(centroid))
                #return rect, centroid #returning the rect features and good feature centroid for future use to send to ev3 or something
       
        elif seg == 'ellipse':
            for ellipse in obj:
                img = cv2.ellipse(img,ellipse,colors[i],2)
                
    return img

def main(argv):
    if len(argv) < 4 | len(argv) > 4:
        print 'Please input image and segmentation type.\n Usage: ColorObjectTracker.py image [minRect|boundRect|ellipse] hsvSettingsFileName'
        raise SystemExit

    file = argv[1]
    seg = argv[2]
    pkl = argv[3]
    
    # readin image:
    img = cv2.imread(file)

    processed_frame = process_frame(img,pkl,seg)
    # Displaying image
    cv2.imshow('processed_frame',processed_frame)
    cv2.waitKey(0)


def run(img,pkl):
    main(['ColorObjectTracker.py',img,'minRect',pkl])

if __name__ == '__main__':
    main(sys.argv)
