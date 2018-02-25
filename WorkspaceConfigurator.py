import cv2
import numpy as np
import cPickle as pickle

global corners, modes, mode
corners = []
modes = ['TopLeft','TopRight','BottomLeft','BottomRight']
show = ['(780,0)','(0,0)','(780,1700)','(0,1700)']
mode = 0

def returnCoordinate(event,x,y,flags,param):
    global corners, mode, modes
    if event == cv2.EVENT_LBUTTONDBLCLK:
        corners.append([x,y])
        print('{} set as : ({},{})'.format(modes[mode],x,y))
        if mode<3:
            mode += 1
        elif mode == 3:
            filename = raw_input('Enter file name: ')
            print('Saving corners to file : {}'.format(filename))
            corners_dictionary = dict(zip(modes,corners))
            print(corners_dictionary)
            f = open(filename,'w')
            pickle.dump(corners_dictionary,f)
            f.close()
            exit
            
    if event == cv2.EVENT_RBUTTONDBLCLK:
        del corners[-1]
        print('Going back to {}'.format(modes[mode]))
        if mode > 0:
            mode -= 1
            
def main():
    global modes, mode
    cap = cv2.VideoCapture(0)
    _ , frame = cap.read()
    cv2.imshow('frame',frame)
    cv2.setMouseCallback('frame',returnCoordinate)
    while True:
        ret, frame = cap.read()
        cv2.putText(frame,show[mode],(10,20),cv2.FONT_HERSHEY_COMPLEX,0.5,\
                        (200,200,200),1)
        cv2.imshow('frame',cv2.flip(frame,1))
        k = cv2.waitKey(10)
        if k == 32:
              break

    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
