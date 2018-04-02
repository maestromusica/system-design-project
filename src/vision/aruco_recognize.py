import cv2
import numpy as np
from GlobalParams import GlobalParams
from Fairies import wsFinder

dict = { 1 : (85,50), 2 : (50,50) , 6 : (80,180)}

def filter(img):
    w,l,_ = np.shape(img)
    image = np.ones( (w,l) )
    for x in range(w):
        for y in range(l):
            b = img[x][y][0]
            g = img[x][y][1]
            r = img[x][y][2]
            if r < 90 and g < 90 and b < 90:
                image[x][y] = 0
    return image

def balance(b,g,r):
    rg = np.abs(r-g)<10
    rb = np.abs(r-b)<10
    gb = np.abs(g-b)<10
    return rg and rb and gb

def extreme(b,g,r):
    small = r < 50 and g < 50 and b < 50
    large = r > 130 and g > 130 and b > 130
    return large or small

def findbox(code,x,y):
    x1,y1 = code[0]
    x2,y2 = code[1]
    x3,y3 = code[2]
    x4,y4 = code[3]
    cx = (x1 + x2 + x3 + x4)/4
    cy = (y1 + y2 + y3 + y4)/4
    l = np.sqrt( (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1) )
    d1 = x1 - cx
    d2 = y1 - cy
    a1 =  0.5*y*( d1 - d2 )/l
    b1 =  0.5*y*( d1 + d2 )/l
    a2 =  0.5*x*( d1 + d2 )/l
    b2 =  0.5*x*( d2 - d1 )/l

    p1 = ( int(cx + a1 + a2) ,int(cy + b1 + b2) )
    p2 = ( int(cx + a1 - a2) ,int(cy + b1 - b2) )
    p3 = ( int(cx - a1 - a2), int(cy - b1 - b2) )
    p4 = ( int(cx - a1 + a2), int(cy - b1 + b2) )

    return p1,p2,p3,p4,cx,cy

def findbox2(code,x,y):
    x1,y1 = code[0]
    x2,y2 = code[1]
    x3,y3 = code[2]
    x4,y4 = code[3]

    # will this give the centroid?? I don't think so. Actually maybe it does.
    cx = (x1 + x2 + x3 + x4)/4
    cy = (y1 + y2 + y3 + y4)/4
    
    a1 = (x2 - x1)*x*0.5 / np.sqrt( (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1) )
    b1 = (y2 - y1)*y*0.5 / np.sqrt( (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1) )

    a2 = (x2 - x3)*x*0.5 / np.sqrt( (x2 - x3)*(x2 - x3) + (y2 - y3)*(y2 - y3) )
    b2 = (y2 - y3)*y*0.5 / np.sqrt( (x2 - x3)*(x2 - x3) + (y2 - y3)*(y2 - y3) )

    p1 = ( int(cx + a1 + a2) ,int(cy + b1 + b2) )
    p2 = ( int(cx + a1 - a2) ,int(cy + b1 - b2) )
    p3 = ( int(cx - a1 - a2), int(cy - b1 - b2) )
    p4 = ( int(cx - a1 + a2), int(cy - b1 + b2) )

    return p1,p2,p3,p4,cx,cy

def main(arg):

    cap = cv2.VideoCapture(0)
    gp = GlobalParams()
    camparams = gp.getCamParams(None)
    workspace = gp.getWorkSpace(None)
    ws = wsFinder(camparams,workspace)

    while True:
       _ , frame = cap.read()
       frame = ws.find(frame)
       dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
       #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       #res = cv2.aruco.detectMarkers(gray,dictionary)


       #if len(res[0]) > 0:
       #    cv2.aruco.drawDetectedMarkers(gray,res[0],res[1])
       #cv2.imshow('gray',gray)

       pts1 = np.float32([[170,9],[437,38],[118,451],[437,466]])
       pts2 = np.float32([[0,0],[320,0],[0,450],[320,450]])
       M = cv2.getPerspectiveTransform(pts1,pts2)
       dst = cv2.warpPerspective(frame,M,(320,450))

       '''## testing
       lower = np.array([0,0,0], dtype="uint8")
       upper = np.array([100,100,100], dtype="uint8")
       mask = cv2.inRange(frame,lower,upper)
       mask = cv2.bitwise_not(mask)
       '''
       res = cv2.aruco.detectMarkers(dst,dictionary)
       if len(res[0]) > 0:
           cv2.aruco.drawDetectedMarkers(dst,res[0],res[1] )
       
       '''
       l = len(res[1])
       for x in range(l):
           code = res[0][x][0]
           id = res[1][x][0]
           cv2.circle(dst,tuple(code[0]),3,(0,255,0),2)
           cv2.circle(dst,tuple(code[1]),3,(0,0,255),2)
           cv2.circle(dst,tuple(code[2]),3,(255,0,0),2)
           cv2.circle(dst,tuple(code[3]),3,(0,255,255),2)
           centroid = np.sum(code,axis=0)/4
#           print('centroid: ({},{})'.format(cx,cy))
           cv2.circle(dst,tuple((centroid)),3,(0,255,255),2)
           
               if id in dict:
                   x,y = dict[id]
                   p1,p2,p3,p4, cx,cy= findbox(code,x,y)
                   'cv2.circle(frame,(cx,cy),3,(0,255,255),2)
                   cv2.line(dst,p1,p2,(255,0,0))
                   cv2.line(dst,p1,p4,(255,0,0))
                   cv2.line(dst,p2,p3,(255,0,0))
                   cv2.line(dst,p4,p3,(255,0,0))
               
           #print('corners:{}{}{}{} '.format(p1,p2,p3,p4))
       '''
       cv2.imshow('frame',frame)
       cv2.imshow('dst',dst)




       k = cv2.waitKey(10)
       if k == 32:
           break

    cv2.destroyAllWindows()


main(0)
