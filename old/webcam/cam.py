import cv2
import numpy as np
import cPickle as pickle
from glob import glob

cap = cv2.VideoCapture(1)

# termination criteria

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,30,0.001)
obj = np.zeros((49,3),np.float32)
obj[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

objpoints = []
imgpoints = []
capture = False

def calibrate(objpoints, imgpoints, shape):
	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(\
	objpoints, imgpoints, shape, None, None)
	print(ret)
	mean_error = 0
	for i in xrange(len(objpoints)):
		imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i]\
				, mtx,dist)
		error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
		mean_error += error
	print("Total error = {}".format(mean_error/len(objpoints)))
	filename = 'intrinsic_params.pkl'
	print 'Saving results to '+ filename
	f = open(filename,'w+')
	'''
	f.write('\n\n writing Ret-error : \n')
	f.write(str(ret))
	f.write('\n\nwriting camera parameters \n')
	f.write(str(mtx))
	f.write('\n\n writing dst:\n')
	f.write(str(dist))
	f.write('\n\n writing rvecs: \n')
	f.write(str(rvecs))
	f.write('\n\n writing tvecs: \n')
	f.write(str(tvecs))
	'''
	pickle.dump(ret,f)
	pickle.dump(mtx,f)
	pickle.dump(dist,f)
	pickle.dump(rvecs,f)
	pickle.dump(tvecs,f)
	
	f.close()

count = 0	

for fname in glob('fra*.png'):
	frame = cv2.imread(fname)
	
	# Converting to gray scale
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	
	# Find the chess board corners
	ret, corners = cv2.findChessboardCorners(gray, (7,7),None)
	
	# If found, add object points, image points 
	if(ret == True):
		objpoints.append(obj)
		
		corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1),criteria)
		imgpoints.append(corners)
		cv2.imwrite('frame-{}.png'.format(count),frame)
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
	
calibrate(objpoints,imgpoints,gray.shape[::-1])
cv2.destroyAllWindows()
	
