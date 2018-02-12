import cv2
import numpy as np
import matplotlib.pyplot as plt
import ColorObjectTracker as cot
import sys
from glob import glob

# Creating nothing function
def nothing(x):
    pass

def main(argv):
    if argv[1] == "demo":
        imgs = glob("images/*.png")
        for img in imgs:
            try:
                cot.run(img)
            except Exception as err:
                print("Error: {}".format(err))
        #cv2.waitKey(0)
    cv2.destroyAllWindows()
    cap = cv2.VideoCapture(0)
    print "Press 'c' for Ready..."

    #stuff for testing
    kernel = np.ones((5,5),np.uint8)
    # Creating trackbars
    cv2.namedWindow('HSV')
    cv2.createTrackbar('H','HSV',0,180,nothing)
    cv2.createTrackbar('S','HSV',0,255,nothing)
    cv2.createTrackbar('V','HSV',0,255,nothing)
    cv2.createTrackbar('Erode','HSV',0,5,nothing)
    cv2.createTrackbar('Dilate','HSV',0,5,nothing)
    #stuff for testing done

    while True:
        _, frame = cap.read()

        #testing for colour seeing
        #masks = getColorMasks(frame)
        #for i,m in enumerate(masks):
        #    cv2.imshow('mask'+str(i),m)
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        # getting values from trackbar
        h = cv2.getTrackbarPos('H','HSV')
        s = cv2.getTrackbarPos('S','HSV')
        v = cv2.getTrackbarPos('V','HSV')
        e = cv2.getTrackbarPos('Erode','HSV')
        d = cv2.getTrackbarPos('Dilate','HSV')
    
        lower = np.array([h,s,v])
        higher = np.array([h+20,255,2550])

        mask = cv2.inRange(hsv,lower,higher)
        mask = cv2.erode(mask,kernel,iterations=e)
        mask = cv2.dilate(mask,kernel,iterations=d)

        cv2.imshow('mask',mask)
        cv2.imshow('img',frame)


        #testing portion done

        #cv2.imshow('frame',frame)
        k = cv2.waitKey(1)
        ##capture an image to process
        if k == ord('c'):
            cv2.imwrite('images/boxes.png',frame)
            break

    cv2.destroyAllWindows()

    #try:
    cot.run('images/boxes.png')
    #except Exception as err:
    #    print("Error: {}".format(err))
    
    #cv2.waitKey(0)

if __name__ == '__main__':
    main(sys.argv)
