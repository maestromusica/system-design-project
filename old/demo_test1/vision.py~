import cv2
import numpy as np
import matplotlib.pyplot as plt
import ColorObjectTracker as cot
import sys
from glob import glob
import Calibrator


def nothing(x):
    pass

def main(argv):

    if argv[1] == "demo":
        imgs = glob("images/*.png")
        for img in imgs:
            try:
                cot.run(img,'demo.pkl')
            except Exception as err:
                print("Error: {}".format(err))
        cv2.destroyAllWindows()
    
    filename = Calibrator.main()
    if filename is None:
	filename = 'demo_final1.pkl'
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        processed_frame, masks = cot.process_frame(frame,filename)
        for i,m in enumerate(masks):
            cv2.imshow('mask'+str(i),m)
        cv2.imshow('frame',frame)
        k = cv2.waitKey(1)
        if k == 32:
            break
        
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
