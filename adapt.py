import numpy as np
import cv2
from glob import glob
import cPickle as pickle
#calibration is for camera matrix stuff
import Calibration as camset
#calibrator is for colour tracking
import Calibrator as clrset
import ColorObjectTracker as cot

#calibrate the camera with chessboards first
boardSize = (9,6)
camset.calibrateCamera(boardSize)

#to make new colour calibration uncomment line VV
clr_prm_file = None
clr_prm_file = clrset.main()
if clr_prm_file is None:
    clr_prm_file = 'demo.pkl'
elif clr_prm_file[-4:] is not '.pkl':
    clr_prm_file = clr_prm_file+'.pkl'

f = open('camera_intrinsic_params.pkl')
optimalmtx = pickle.load(f)
mtx = pickle.load(f)
distcoeffs = pickle.load(f)
#rvecs = pickle.load(f)
#tvecs = pickle.load(f)
f.close()

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    #undistortion using the calibration parameters
    corrected_img = cv2.undistort(src=frame, cameraMatrix=mtx, distCoeffs=distcoeffs, newCameraMatrix=optimalmtx)
    #perspective transform of the boxes
    #find the points by the corners (find the corners of the work area) in the corrected image
    pts1 = np.float32([[200,20],[420,30],[150,470],[415,475]])
    #to an img the size of the work area millimetres or possibly centimetres
    #depends on accuracy of hardware, how close we can get to exactly coords
    pts2 = np.float32([[0,0],[200,0],[0,500],[200,500]])
    #this is the matrix we need to transform points with M.dot(vector)
    #point = [100, 100, 1] -- last coordinate is homogeneous coord 1
    #x, y, z = M.dot(point)
    M = cv2.getPerspectiveTransform(pts1,pts2)
    pers_img = cv2.warpPerspective(corrected_img,M,(200,500))

    #show the different imgs

    cv2.imshow('frame',frame)
    cv2.imshow('corrected',corrected_img)
    cv2.imshow('perspective transform', pers_img)

    #do colour object tracking on the perspective transform img
    #these should be the rl coords then because they're from the transformed image

    k = cv2.waitKey(1)
    if k == ord('c'):
        cv2.imwrite('Images/boxes.png',pers_img)
        cot.run('Images/boxes.png', clr_prm_file)
        f = open('objects.pkl')
        boxes = pickle.load(f)
        for box in boxes:
            print('Centroid: '+ str(box[1]))
        f.close()
        break        
    elif k == 32:
        break

cv2.destroyAllWindows()
