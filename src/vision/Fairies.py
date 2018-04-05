import cv2
import numpy as np
from base import MaskGenerator, ContourExtractor, CornersDetector, Drawer
from collections import Counter

global data
data = {
    1:{'type':'blue','destination':'Edinburgh','weight':5},\
    2:{'type':'yellow','destination':'London','weight':3},\
    3:{'type':'pink','destination':'Edinburgh','weight':2},\
    4:{'type':'red','destination':'Glasgow','weight':5},\
    5:{'type':'orange','destination':'Glasgow','weight':1},\
    6:{'type':'green','destination':'Edinburgh','weight':1}}



###################### HELPER FUNCTIONS ###################################

'''
Function to flip the detections horizontally for aruco detections.
'''
def flipX(point,shape):
    # flips the x axis. required for detection
    return (int(shape[1] - point[0]-1),int(point[1]))


'''
Function to extract the area of the image containing the Detected colour box.
'''
def findRoi(frame, box):
    
    min_x = np.min(box[:,0])
    max_x = np.max(box[:,0])
    min_y = np.min(box[:,1])
    max_y = np.max(box[:,1])
    h,w,c = frame.shape
    mask = np.zeros((h,w),np.uint8)
    mask[min_y:max_y, min_x:max_x] = 255
    frame = cv2.bitwise_and(frame,frame,mask=mask)
    return frame

'''
Function to find the orientation depending on the colour box detection measurements.
@return : 90.00 : vertical
        : 00.00 : horizontal
'''
def findOrientation(box,angle):
    retval = angle
    if(angle < 2 and angle > -10 or (angle > -90 and angle < -80) ):
        diff_x = 0
        diff_y = 0
        for i,b in enumerate(box):
            for c in box[i+1:]:
                diff = np.abs(b[0] - c[0])
                if diff > diff_x:
                    diff_x = diff
                    diff = np.abs(b[1] - c[1])
                if diff > diff_y:
                    diff_y = diff
        if diff_x > diff_y:
            retval = 0.00
        elif diff_y > diff_x:
            retval = 90.00
    return retval


'''
Function to find the orientation depending on the orientation of the aruco code.
@return : 90.00 : vertical
        : 00.00 : horizontal
'''
def findOrientationAruco(corners):
    x,y = corners[0]
    left = False
    top = False
    checkx = np.where(np.sort(corners[:,0]) == x)[0][0]
    checky = np.where(np.sort(corners[:,1]) == y)[0][0]
    
    if checkx < 2 :
        left = True
    if checky < 2:
        top = True

    if (top and left) or (not(top) and not(left)):       
        return 0.00
    else:
        return 90.00



########################## CLASSES ##########################################
    
#class for finding the workspace out of a big image thing
class WorkspaceFinder(object):

    def __init__(self,camParams, ws):
        self.optmtx = camParams['optmtx']
        self.mtx = camParams['mtx']
        self.dist = camParams['distcoeffs']
        #put workspace vals into order points from and to
        From, To = [], []
        for k, v in ws.items():
            From.append(v[0])
            To.append(v[1])
        self.ptsFrom, self.ptsTo = np.float32(From), np.float32(To)
        
        self.wsSize = (ws['BottomRight'][1][0],ws['BottomRight'][1][1])


    def find(self,img):
        #undistort the image
        corrected_image = cv2.undistort(src=img, cameraMatrix=self.mtx, distCoeffs=self.dist, newCameraMatrix=self.optmtx)
        #get perspective transform matrix
        M = cv2.getPerspectiveTransform(self.ptsFrom,self.ptsTo)
        #crop image
        cropped_img = cv2.warpPerspective(img,M,self.wsSize)
        return cropped_img



#class for finding the masks from the workspace image
class MaskFinder(object):

    def __init__(self,maskVals):
        self.maskGenerators = {}
        for k, v in maskVals.items():
            self.maskGenerators.update({k:MaskGenerator(maskVals[k],k)})
        

    def find(self,img):
        masks = {}
        for k, m in self.maskGenerators.items():
            masks.update({k:m.extractMask(img)})
        return masks

# class for finding aruco markers
class ArucoFinder(object):
    def __init__(self):
        self.dict_val = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        
    def findMarkers(self,frame,draw=False):
        
        # Need to flip the frame because aruco markers are not immune to lateral
        # inversion.
        
        flip = cv2.flip(frame,1)        
        res = cv2.aruco.detectMarkers(flip,self.dict_val)
        # if aruco markers found
        codes = {}
        info = {}
        if (len(res[0])  > 0):
            for x in range(len(res[1])):
                aruco_id = res[1][x][0]
                # extracting corners
                corners = res[0][x][0]

                # flipping corners again 
                for i,p in enumerate(corners):                    
                    p = flipX(p,frame.shape)
                    corners[i]=p

                # calculating centroid
                centroid = np.sum(corners,axis=0)/4

                # forming data dictionary
                info['corners'] = corners
                info['centroid'] = centroid
                codes[aruco_id] = info.copy()
                if draw:
                    cv2.circle(frame,tuple(centroid),2,(0,0,0),2)
            
            if draw == True:
                cv2.aruco.drawDetectedMarkers(frame,res[0],res[1])

            return codes,frame

        return None, frame


#class for finding boxes in the workspace img
class BoxFinder(object):
    
    def __init__(self, quality):
        self.contourExtractor = ContourExtractor()
        self.cornersDetector = CornersDetector(quality=quality)
        self.arucoFinder = ArucoFinder()
        self.drawer = Drawer()

    # function to create a dictionary representing a box.
    def createDict(self,centroid,colour,rotation,destination = None):
        '''
        if dim[0] > dim[1]:
            length = dim[0]
            width = dim[1]
        else:
            length = dim[1]
            width = dim[0]
        '''
        return {'centroid':centroid,'colour':colour,'rotation':rotation,'destination':destination}

    # function to use colour and aruco detection
    # should be used under the assumption that box spatial info (centroid,corners)
    # are estimated using colour based detection and aruco codes can be anywhere on the top
    # surface of box.
    def find(self, img, masks):
        # creating a copy to draw points and edges
        draw = img.copy()

        # list to store boxes as a dictionary
        boxes = []

        # For each colour mask
        for k, m in masks.items():
            #cv2.imshow('mask-'+k,m)
            # Find Box Contours
            contours = self.contourExtractor.segmentation(m)

            # if Contours exist
            if len(contours) > 0:
                valid = 0
                # for each box candidate
                for box, rect in contours:
                    
                    # extracting roi for aruco detection
                    roi = findRoi(img,box)
                    aruco_codes, roi = self.arucoFinder.findMarkers(roi,draw=False)
#                    cv2.imshow('roi',roi)
#                    cv2.waitKey(100)
                    # Note, Since we are finding codes for each box candidate
                    # we will only use the first aruco code we find.
                    
                    if aruco_codes is not None:
                        if len(list(aruco_codes.keys()))>1:
                            print('Found more than one aruco codes. Please check the "conflict" window.')
                            cv2.imshow('conflict',roi)
                            cv2.waitKey(0)
                            cv2.destroyWindow('conflict')
                        
                        aruco_code = list(aruco_codes.keys())[0]
                        cv2.circle(draw,tuple(aruco_codes[aruco_code]['corners'][0]),2,(255,0,0),2)
                        cv2.circle(draw,tuple(aruco_codes[aruco_code]['corners'][1]),2,(255,255,0),2)
                        cv2.circle(draw,tuple(aruco_codes[aruco_code]['corners'][2]),2,(0,0,255),2)
                        cv2.circle(draw,tuple(aruco_codes[aruco_code]['corners'][3]),2,(0,255,255),2)
                        cv2.circle(draw,tuple(aruco_codes[aruco_code]['centroid']),2,(0,255,0),2)
                        valid += 1
                        
                    else:
                        
                        # if aruco marker not find. Detection is noise. skip to next box candidate.
                        # drawing false positives with red.
                        draw = self.drawer.drawBox(draw,box,np.array(rect[0]),'r')
                        continue
                    
                    # find orientation of the box.
                    angle = findOrientation(box,rect[2])

                    # form box dictionary
                    boxes.append(self.createDict(rect[0],k,angle,data[aruco_code]['destination']))

                    # Draw true positives with blue.
                    draw = self.drawer.drawBox(draw,box,np.array(rect[0]),'b')
                    valid +=1
                draw = self.drawer.putText(draw,k,valid,angle,None)
                    
        return draw, boxes

    # Function to detect boxes only using the aruco codes under the assumption that
    # aruco codes are centre aligned with the top layer of the box.( Centroid of the box is
    # same as the centroid of the aruco code.)
    def findAruco(self,image):

        # find all the aruco codes in the image.
        aruco_codes , image= self.arucoFinder.findMarkers(image,draw=False)
        boxes = []
        count = Counter()
        orientations = {}
        destinations = {}
        if aruco_codes is not None:
            # keys are the aruco_ids of each box.
            for k in list(aruco_codes.keys()):

                # get data using the aruco_id
                metadata = data[k]

                # get spatial_info(corners,centres in the image)
                spatial_info = aruco_codes[k]
                
                # calculate orientations
                orientation = findOrientationAruco(spatial_info['corners'])

                if spatial_info['centroid'][1] > 330:
                # form box dictionary
                    boxes.append(self.createDict(spatial_info['centroid'],\
                                         metadata['type'],orientation,\
                                         metadata['destination']))
            
                    # book keeping
                    count[metadata['type']] += 1;
                    orientations[metadata['type']] = orientation
                    destinations[metadata['type']] = metadata['destination']
                    
                    cv2.circle(image,tuple(spatial_info['corners'][0]),2,(255,0,0),2)
                    cv2.circle(image,tuple(spatial_info['corners'][1]),2,(255,255,0),2)
                    cv2.circle(image,tuple(spatial_info['corners'][2]),2,(0,0,255),2)
                    cv2.circle(image,tuple(spatial_info['corners'][3]),2,(0,255,255),2)
                    cv2.circle(image,tuple(spatial_info['centroid']),2,(0,255,0),2)
                    
            # Draw data on the frame.
            for k in list(count.keys()):
                self.drawer.putText(image,k,count[k],orientations[k],destinations[k])


            return image, boxes

        else:
            return image, None
