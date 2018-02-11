import numpy as np
import cv2
from glob import glob
import cPickle as pickle

def getCamera(imgs, boardSize):
    #imgs is a list of image file names and board size is a tuple (x,y)
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((boardSize[0]*boardSize[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:boardSize[0],0:boardSize[1]].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    for i in imgs:
        img = cv2.imread(i)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, boardSize,None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners)

            # Draw and display the corners
            cv2.drawChessboardCorners(img, boardSize, corners,ret)
            cv2.imshow(i,img)
            cv2.waitKey(500)
        else:
            print "No Chessboard Detected in {}".format(i)

    cv2.destroyAllWindows()

    ret, mtx, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

    h,  w = img.shape[:2]
    newcameramtx, _ = cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    return newcameramtx, mtx, dist

def main():
	# getting file names
	files = glob('Images/f*.png')
	boardSize = (7,7)
	
	# Getting Camera matrix	
	optimal_matrix, mtx, dist = getCamera(files, boardSize)

	f = open('camera_intrinsic_params.pkl','w')
    	pickle.dump(optimal_matrix,f)
   	pickle.dump(mtx,f)
        pickle.dump(dist,f)
        print('Saved params to file : camera_intrinsic_params.pkl')
        f.close()

if __name__ == '__main__':
	main()
