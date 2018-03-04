import numpy as np
import cv2
from glob import glob
import cPickle as pickle

def runChess(boardSize):
    cap = cv2.VideoCapture(0)

    # termination criteria

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,30,0.001)
    obj = np.zeros((boardSize[0]*boardSize[1],3),np.float32)
    obj[:,:2] = np.mgrid[0:boardSize[0],0:boardSize[1]].T.reshape(-1,2)
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
        ret, corners = cv2.findChessboardCorners(gray, boardSize,None)

        # If found, add object points, image points 
        if(ret == True and capture == True):
            objpoints.append(obj)

            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            cv2.imwrite('Images/frame-{}.png'.format(count),frame)
            cv2.drawChessboardCorners(frame,boardSize, corners2, ret)
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

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

    h,  w = img.shape[:2]
    newcameramtx, _ = cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    return newcameramtx, mtx, dist, rvecs, tvecs

def calibrateCamera(boardSize):

    #runChess(boardSize)

    # getting file names
    files = glob('Images/f*.png')
    
    # Getting Camera matrix
    optimal_matrix, mtx, dist, rvecs, tvecs = getCamera(files, boardSize)


    # Added for integration for @ruth
    return {'optmtx':optimal_matrix,'mtx':mtx,'distcoeffs':dist}
    
    
    #f = open('camera_intrinsic_params.pkl','w')
    #print(optimal_matrix)
    #pickle.dump(optimal_matrix,f)
    #print(mtx)
    #pickle.dump(mtx,f)
    #print(dist)
    #pickle.dump(dist,f)
    #print(rvecs)
    #pickle.dump(rvecs,f)
    #print(tvecs)
    #pickle.dump(tvecs,f)
    #print('Saved params to file : camera_intrinsic_params.pkl')
    #f.close()

