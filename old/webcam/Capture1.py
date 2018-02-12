import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# termination criteria

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,30,0.001)
obj = np.zeros((49,3),np.float32)
obj[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)
count = 0
objpoints = []
imgpoints = []
capture = False

while True:
	ret, frame = cap.read()
	#frame = cv2.imread(fname)
	
	# Converting to gray scale
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	
	# Find the chess board corners
	ret, corners = cv2.findChessboardCorners(gray, (7,7),None)
	
	# If found, add object points, image points 
	if(ret == True and capture == True):
		objpoints.append(obj)
		
		corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1),criteria)
		imgpoints.append(corners)
		cv2.imwrite('Images/frame-{}.png'.format(count),frame)
		cv2.drawChessboardCorners(frame,(7,7), corners2, ret)
		cv2.imshow('detected-corners',frame)
                count += 1
		capture = False
		
		if count == 10:
			break
	cv2.imshow('frame',frame)
	
	k = cv2.waitKey(1)
	if (k == ord('c')):
        	capture = not capture
	if( k ==  32):
		break
	
#calibrate(objpoints,imgpoints,gray.shape[::-1])
cv2.destroyAllWindows()
