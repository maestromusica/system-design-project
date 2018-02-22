#!/usr/bin/env python

'''
USAGE : ./Calibrate.py

During the program use the following buttons:
        '<' or '>' to toggle between display modes:[frame,hsv,mask,res](Top right).
        't' to toggle colour mode.[red,yellow,green,blue] (Top left)
        'c' to save the current configuration for the colour mode.
        's' to dump the saved configurations into a pickle file.
        'p' to increase gamma correction(TOP CENTER)
        'o' to decrease gamma correction(TOP CENTER)
        'b' to return color_conf dictionary and exit.(Added for Integration on request of @ruth)
        'q' to take a screenshot of current display image and save it to a file.
        '[space]' to exit.
        
'''

from __future__ import print_function
import cv2
import numpy as np
import cPickle as pickle

# Declaring Global variables

global trackbars, colormodes, displaymodes
trackbars = False
colormodes = np.array(['red','yellow','green','blue','purple'])
displaymodes = np.array(['frame','gamma','hsv','mask','res'])

# functions

def nothing(x):
    pass

def createParameters():
    params = {}
    params['gamma'] = 0
    params['H_min'] = 179
    params['H_max'] = 179
    params['S_min'] = 255
    params['S_max'] = 255
    params['V_min'] = 255
    params['V_max'] = 255
    params['Erode'] = 5
    params['Dilate'] = 5
    params['open:1 / close:0'] = 1
    params['blur'] = 5

    return params

def createTrackbars(params,name='HSV'):
    cv2.namedWindow(name)
    global trackbars
    trackbars = True
    for k in sorted(params.keys()):
        if params[k] is not 0:
            cv2.createTrackbar(k,name,0,params[k],nothing)
        
def readTrackbars(params,name='HSV'):
    global trackbars
    if trackbars == True:
        for k in params.keys():
            if k != 'gamma':
                params[k] = cv2.getTrackbarPos(k,name)
    else:
        print('Trackbars not created. First create Trackbars.')
            
    return params

def open_close(mask,kernel,params):
    if params[params.keys()[-1]] == 1:
        mask = cv2.erode(mask,iterations = params['Erode'],kernel = kernel)
        mask = cv2.dilate(mask,iterations = params['Dilate'],kernel = kernel)
    elif params[params.keys()[-1]] == 0:
        mask = cv2.dilate(mask,iterations = params['Dilate'],kernel = kernel)
        mask = cv2.erode(mask,iterations = params['Erode'],kernel = kernel)
    return mask

def toggleMode(mode):
    if mode == 'red':
        mode = 'yellow'
    elif mode == 'yellow':
        mode = 'green'
    elif mode == 'green':
        mode = 'blue'
    elif mode == 'blue':
        mode = 'purple'
    elif mode == 'purple':
        mode = 'red'
    return mode

#def toggleDisplayMode(mode)
    

def checkParams(params):
    global colormodes
    if len(params.keys()) == len(colormodes):
        return True, None
    else:
        bools = np.array([i in params.keys() for i in colormodes])
        incomplete = colormodes[np.where(bools == False)]
        return False, incomplete

def dumpConfiguration(params,filename):
    if filename[-4:]!='.pkl':
        filename = filename+'.pkl'
    f = open(filename,'w')
    pickle.dump(params,f)
    f.close()
    print('Color_configuration saved to file : {}'.format(filename))
    print('use `params = pickle.load(file)` to access contents.')
    print('Contents:')
    print(params)
    

def display(colormode,mode,images,gamma):
    cv2.putText(images[mode],colormode,(5,20),cv2.FONT_HERSHEY_COMPLEX,1,\
                    (200,200,200),2)
    cv2.putText(images[mode],displaymodes[mode],(500,20),cv2.FONT_HERSHEY_COMPLEX,1,\
                    (200,200,200),2)
    cv2.putText(images[mode],str(gamma),(250,20),cv2.FONT_HERSHEY_COMPLEX,1,\
                    (200,200,200),2)
    cv2.imshow('calibrate',images[mode])

def gamma_correct(img,gamma):
    img = img/255.0
    img = cv2.pow(img,gamma)
    return np.uint8(img*255)

def main():
    print(gamma_correct)
    # Flag for return
    flag = False
    # Varibale to represent current colour mode:
    colorMode = 'red'
    displayMode = 0

    # dictionary to store params for each color
    color_conf = {}
    params = createParameters()
    
    # Creating Trackbars for Calibration.
    createTrackbars(params)
    
    # creatin camera object
    cap = cv2.VideoCapture(0)

    # Creating kernel element for erosion/dilation
    kernel = np.ones((5,5))
    
    # Infinte Processing Loop
    while True:
        ret, frame = cap.read()

        # updating values
        params = readTrackbars(params)

        blur = frame.copy()
        for _ in xrange(params['blur']):
            blur = cv2.bilateralFilter(blur,9,75,75)

        gamma = gamma_correct(blur,params['gamma'])
        
        # converting to hsv for filtering.
        hsv = cv2.cvtColor(gamma,cv2.COLOR_BGR2HSV)

        # creating ranges
        lower = np.array([params['H_min'],params['S_min'],params['V_min']])
        upper = np.array([params['H_max'],params['S_max'],params['V_max']])
    
        # filtering image.
        mask = cv2.inRange(hsv,lower,upper)

        # Applying erosion and dilation
        mask = open_close(mask,kernel,params)

        # result
        res = cv2.bitwise_and(frame,frame,mask=mask)

        images = [frame,gamma,hsv,mask,res]
        # displaying images
        display(colorMode,displayMode,images,params['gamma'])
        
        # Adding text to frame to represent current filtering mode.
        k = cv2.waitKey(1)
        if k == ord(' '):
            break
        elif k == ord('t'):
            colorMode = toggleMode(colorMode)
        elif k == ord('c'):
            color_conf[colorMode] = params.copy()
            print(color_conf)
        elif k == ord('s'):
            ret, incomplete = checkParams(color_conf)
            if ret:
                filename = raw_input('Enter name for the configuration file: ')
                dumpConfiguration(color_conf,filename)
		flag = True
                break
            else:
                print('Color Configuration incomplete.')
                print('Please complete configuration for following colors: {}'\
                      .format(incomplete))
        
        elif k == ord('b'):
            return color_conf

        elif k == ord('<'):
            if displayMode == 0:
                displayMode = 4
            else:
                displayMode -= 1

        elif k == ord('>'):
            if displayMode == 4:
                displayMode = 0
            else:
                displayMode += 1
        elif k == ord('p'):
            params['gamma'] += 0.1
        elif k == ord('o'):
            params['gamma'] -= 0.1
        elif k == ord('q'):
            filename = str(raw_input('Enter filename: '))
            cv2.imwrite(filename,images[displayMode])
            
    cv2.destroyAllWindows()
    cap.release()
    if flag:
        return filename
    else:
        return None 
if __name__ == '__main__':
    print(__doc__)
    main()
