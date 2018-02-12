import cv2
import numpy as np
import cPickle as pickle
from glob import glob

filename = 'camera_intrinsic_params.pkl'
f = open(filename,'r')
optimal_matrix = pickle.load(f)
mtx = pickle.load(f)
dist = pickle.load(f)
f.close()

def draw(img,corners,imgpts):
	corner = tuple(corners[0].ravel())
	img = cv2.line(img,corner,tuple(imgpts[0].ravel()), (255,0,0),5)
	img = cv2.line(img,corner,tuple(imgpts[1].ravel()), (0,255,0),5)
	img = cv2.line(img,corner,tuple(imgpts[2].ravel()), (0,0,255),5)
	return img

cap = cv2.VideoCapture(0)

# Setting criterias

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((9,3),np.float32)
objp[:,:2] = np.mgrid[0:3,0:3].T.reshape(-1,2)

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

count = 0;
while True:
	# polling for frame
	ret , frame = cap.read()

	# converting to gray scale
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	
	# finding chessboard corners
	
	ret, corners = cv2.findChessboardCorners(gray, (3,3), None)
	
	if( ret == True) :
	    corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
	    
	    # Findin rotation and translation vectors;
	    ret,rvecs, tvecs ,inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)
	    
	    # project 3d points to image plane
	    imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
	    
	    pose = draw(frame.copy(),corners2,imgpts)
	    cv2.imshow('pose',pose)
	

        cv2.imshow('frame',frame)
	k = cv2.waitKey(1)
	if k==32:
		break

cv2.destroyAllWindows()
