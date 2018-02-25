import cv2
import numpy as np
import cPickle as pickle
import sys
import json

class MaskGenerator(object):
    '''
    class to extract masks from an image given initialisation parameters.
    The initilisation parameters are a dictionary from Calibrator.py class.
    '''
    def __init__(self,params,colour):
        self.colour = colour
        self.params = params
        #self.low = np.array(params['Low'])
        #self.high = np.array(params['High'])
        self.low = np.array([params['H_min'],params['S_min'],params['V_min']])
        self.high = np.array([params['H_max'],params['S_max'],params['V_max']])
    
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        print('Created MaskGenerator object for {} colour.'.format(colour))
        print('\t Parameters : {}'.format(self.params))

    def setParam(self,att_name,val):
        if att_name in self.params.keys():
            self.params[att_name] = val
            return True
        else:
            print('Error: {} is not a parameter.'.format(att_name))
            return False

    def getParam(self,att_name):
        if att_name in self.params.keys():
            return self.params[att_name]
        else:
            print('Error: {} is not a parameter.'.format(att_name))
            return None

    @staticmethod
    def gammaCorrect(img,gamma):
        img = img/255.0
        img = cv2.pow(img,gamma)
        return np.uint8(img*255)

    def openOrClose(self,mask,kernel):
        isopen = self.params[self.params.keys()[-1]]
        if isopen == 1:
            mask = cv2.erode(mask,iterations = self.params['Erode'],kernel = kernel)
            mask = cv2.dilate(mask,iterations = self.params['Dilate'],kernel = kernel)
        elif isopen == 0:
            mask = cv2.dilate(mask,iterations = self.params['Dilate'],kernel = kernel)
            mask = cv2.erode(mask,iterations = self.params['Erode'],kernel = kernel)
        return mask

    def extractMask(self,frame):
        '''
        Method to Extract Mask from the params.

        Returns a binary image of same size as frame
        '''

        # creating a copy of frame to process.
        frame_blurred = frame.copy()

        # Applying blurring for params['blur'] iterations.
        for _ in xrange(self.params['blur']):
            frame_blurred = cv2.bilateralFilter(frame_blurred,9,75,75)

        # Applying Gamma Correction.
        gammaCorrectedFrame = MaskGenerator.gammaCorrect(frame_blurred,self.params['gamma'])

        # Converting to HSV colour Space
        hsv = cv2.cvtColor(gammaCorrectedFrame,cv2.COLOR_BGR2HSV)

        # Filtering using set parameters
        mask = cv2.inRange(hsv,self.low,self.high)

        # Applying Morphological Operations
        mask = self.openOrClose(mask,self.kernel)

        return mask

''' Creating Class for Contour Extraction and Segmentation of Boxes. '''

class ContourExtractor(object):
    '''Class to extract Contours and fit a shape depending on the segmentation param'''

    def __init__(self,seg = 'minRect'):
        # Validating Segmentation Param
        if(seg == 'minRect' or seg == 'boundRect' or seg == 'ellispe'):
            self.seg = seg
        else:
            print('Invalid Segmentation Param : {}. Setting Segmentation Param to `minRect`'.format(seg))
            self.seg = 'minRect'

    @staticmethod
    def max_area_contour(mask):
        # using cv2.RETR_EXTERNAL because this only returns the outer most contours in
        # a heirarchy of contours. (Solves box within a box problem)
        _,contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        max_area = 2000
        select = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                select.append(cnt)
        return select

    @staticmethod
    def extractBoundingRect(mask):

        contours = ContourExtractor.max_area_contour(mask)
        dims = []
        for cnt in contours:
            # finding enclosing rectangle
            x,y,w,h = cv2.boundingRect(cnt)
            dims.append((x,y,w,h))
        return dims

    @staticmethod
    def extractMinAreaRect(mask):
        contours = ContourExtractor.max_area_contour(mask)
        boxes = []
        for cnt in contours:
            # finding minimum area rect
            rect = cv2.minAreaRect(cnt)
            w,h = np.array(rect[1])
            #h += 5; w+=5;
            #box = cv2.boxPoints((rect[0],(w,h),rect[2]))
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            boxes.append((box,rect))
        return boxes

    @staticmethod
    def fit_ellipse(mask):
        contours = ContourExtractor.max_area_contour(mask)
        ellipses = []
        for cnt in contours:
            ellipses.append(cv2.fitEllipse(cnt))
        return ellipses

    def segmentation(self,mask):
        '''
        Method returns a list of Box Candidates.
        Each Candidate has corners, centroid,
        '''
        if self.seg == 'ellipse':
            return ContourExtractor.fit_ellipse(mask)

        elif self.seg == 'boundRect':
            return ContourExtractor.extractBoundingRect(mask)

        elif self.seg == 'minRect':
            return ContourExtractor.extractMinAreaRect(mask)

'''
Creating Class to detect corners in the region of Candidate Boxes.
'''

class CornersDetector(object):
    def __init__(self,quality = 0.03):
        self.quality = quality
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

    def arrangeCorners(self,corners):
        '''
        This function arranges the Corners in a clockwise fashion.
        This function is important for correct estimation of pose of the boxes.
        '''
        return sorted(corners, key= lambda x:(x[0],x[1]))


    def findGoodFeaturesToTrack(self,img,box):
        # Converting to grayscale for cornerdetection
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

        # Detecting Corners using Shi-tomasi Algorithm
        corners = cv2.goodFeaturesToTrack(gray,50,self.quality,10)

        if corners is not None:

            corners = corners.flatten().reshape(-1,2)

            # Refining Corners at Subpixel Level
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.01)
            corners = cv2.cornerSubPix(gray,corners,(5,5),(-1,-1),criteria)

            # finding candidate Corners from all the corners detected
            corners = self.findNearestPoints(box,corners)

            if len(corners) == 4:
                # rearranging Corners:
                corners = self.arrangeCorners(corners)
                centroid = np.sum(corners,axis=0)/4
            else:
                print("Not Enough Corners: {}".format(corners))
            return corners, centroid

        else:
            print "No corners found."
            return None,None

    def findNearestPoints(self,box, corners):
        '''
        This method finds four candidate Corners which are nearest to
        the corners of the bounding box found from ContourExtractor Class..
        '''
        best_corners = box.copy()
        for i,b in enumerate(box):
            min_dist = 10000
            for j,c in enumerate(corners):
                d = np.linalg.norm(c-b)
                if d<min_dist:
                    best_corners[i] = c
                    min_dist = d
        return best_corners

    def detectCorners(self,frame,mask,box):
        # Dilating mask to make sure that edges and corners of boxes are included.
        mask = cv2.dilate(mask,iterations=3,kernel = self.kernel)

        # extracting ROI
        roi = cv2.bitwise_and(frame,frame,mask = mask)

        # Finding Corners and Centroid of the box.
        corners , centroid = self.findGoodFeaturesToTrack(roi,box)

        if corners is not None:
            return corners, centroid
        else:
            print('CornersDetector::detectCorners() : No Corners Found.')
            return None, None

class Drawer(object):
    ''' Class to draw boxes on input frame '''
    def __init__(self):
        self.colors = {'r':[0,0,255],'g':[0,255,0],'b':[255,0,0]}
    
    def drawBox(self,frame,corners,centroids,color='r'):
        for z in corners:
            x,y = z.ravel()
            cv2.circle(frame,(x,y),3,[0,0,255],-1)
        cv2.circle(frame,tuple(np.int0(centroids)),2,[255,0,0],-1)
            #print("Centroid X-Coordinate: %.2f and Y-Coordinate: %.2f" % (centroid[0], centroid[1]))
            #cv2.line(frame,tuple(corners[0]),tuple(corners[3]),[0,0,255],1)
            #cv2.line(frame,tuple(corners[1]),tuple(corners[2]),[0,0,255],1)

        frame  = cv2.drawContours(frame,[np.array(corners)],0,self.colors[color],1)
        return frame
    def putText(self,frame,colour,val):
        if colour == 'red':
            cv2.putText(frame,colour + ' : {}'.format(val),(10,20),cv2.FONT_HERSHEY_COMPLEX,0.5,\
                        (200,200,200),1)
        elif colour == 'yellow':
            cv2.putText(frame,colour + ' : {}'.format(val),(140,20),cv2.FONT_HERSHEY_COMPLEX,0.5,\
                        (200,200,200),1)
        elif colour == 'green':
            cv2.putText(frame,colour + ' : {}'.format(val),(260,20),cv2.FONT_HERSHEY_COMPLEX,0.5,\
                        (200,200,200),1)
        elif colour == 'purple':
            cv2.putText(frame,colour + ' : {}'.format(val),(360,20),cv2.FONT_HERSHEY_COMPLEX,0.5,\
                        (200,200,200),1)
        elif colour == 'blue':
            cv2.putText(frame,colour + ' : {}'.format(val),(460,20),cv2.FONT_HERSHEY_COMPLEX,0.5,\
                        (200,200,200),1)
        return frame

class PerspectiveTransform(object):
    '''
    Class to change perspective of the input image to an image that restricts itself to \
    the workspace of the robot.
    '''
    def __init__(self,camParams,workspace):

        self.optimal_mtx = camParams['optmtx']
        self.camera_mtx = camParams['mtx']
        self.distcoeffs = camParams['distcoeffs']
        
        pts1 = []
        pts2 = []
        for k in workspace.keys():
            print k
            pts1.append(workspace[k][0])
            pts2.append(workspace[k][1])
        self.original_points = np.float32(pts1)
        self.transformed_points = np.float32(pts2)
        print(self.original_points)
        print(self.transformed_points)
    def transform(self,frame):
        corrected_img = cv2.undistort(src=frame, cameraMatrix=self.camera_mtx, distCoeffs=self.distcoeffs, newCameraMatrix=self.optimal_mtx)
        #perspective transform of the boxes
        #find the points by the corners (find the corners of the work area) in the corrected image

        #pts1 = np.float32([[200,20],[420,30],[150,470],[415,475]])
        #to an img the size of the work area millimetres or possibly centimetres
        #depends on accuracy of hardware, how close we can get to exactly coords
        #pts2 = np.float32([[0,0],[200,0],[0,500],[200,500]])
        #this is the matrix we need to transform points with M.dot(vector)
        #point = [100, 100, 1] -- last coordinate is homogeneous coord 1
        #x, y, z = M.dot(point)
        M = cv2.getPerspectiveTransform(self.original_points,self.transformed_points)

        return cv2.warpPerspective(corrected_img,M,(400,850))
    
##class for box objects
class Box(object):
    '''
    Class to create objects of detected boxes.
    '''

    def __init__(self,(cx,cy),length,width,colour,rotation):
        self.centroid = (cx,cy)
        self.length = length
        self.width = width
        self.colour = colour
        self.rotation = rotation


    def getDetails(self):
        detail = {}
        detail['centroid'] = self.centroid
        detail['colour'] = self.colour
	detail['length'] = self.length
	detail['width'] = self.width
	detail['rotation'] = self.rotation
        detail_json = json.dumps(detail)
        return detail_json

    def __str__(self):
        print('Box:: [colour: {} | centroid : {} ]'.format(self.centroid,self.colour))


class BoxExtractor(object):
    '''The Primary class that the controller will talk with. '''
    def __init__(self,maskParam,camParam,workspace,seg='minRect',quality=0.5):

        self.changePerspective = PerspectiveTransform(camParam,workspace)
        self.colours = maskParam.keys()
        self.boxes = {}
        # Creating Mask Generator Objects for each Colour.
        self.maskGenerators = {}
        for c in self.colours:
            self.maskGenerators[c] = MaskGenerator(maskParam[c],c)
            
        self.contourExtractor = ContourExtractor(seg)
        self.cornersDetector = CornersDetector(quality=quality)
        self.drawer = Drawer()



    def processImage(self, frame):
        changed_image = self.changePerspective.transform(frame)
        draw = changed_image.copy()
        for c in self.colours:
            boxes= []
            mask = self.maskGenerators[c].extractMask(changed_image)
            cv2.imshow('mask-{}'.format(c),mask)
            contours = self.contourExtractor.segmentation(mask)
            if len(contours) > 0:
                for box,rect in contours:
                    corners,centroid = self.cornersDetector.detectCorners(changed_image,mask,box)
                    #draw = self.drawer.drawBox(draw,corners,centroid,'r')
                    draw = self.drawer.drawBox(draw,box,np.array(rect[0]),'b')
                    boxes.append(Box(rect[0],box,c,rect[2]))
                self.boxes[c] = boxes
                draw = self.drawer.putText(draw,c,len(boxes))
            #else:
                #print('No Boxes')

        return draw, self.boxes

def main(argv):
    param = argv[1]
    cap = cv2.VideoCapture(0)
    bx = BoxExtractor(param)

    while True:
       _ , frame = cap.read()

       cv2.imshow('frame',frame)
       res, boxes = bx.processImage(frame)
       cv2.imshow('result',res)
       print(boxes)
       k = cv2.waitKey(10)
       if k == 32:
           break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
