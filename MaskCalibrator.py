import cv2
import numpy as np

'''
USAGE : ./Calibrate.py

During the program use the following buttons:
        '<' or '>' to toggle between display modes:[frame,gamma,hsv,mask,res](Top right).
        't' to toggle colour mode.[red,yellow,green,blue,purple] (Top left)
        'c' to set the current values for the colour mode.
        'p' to increase gamma correction(TOP CENTER)
        'o' to decrease gamma correction(TOP CENTER)
        's' to exit saving configuration values
        '[space]' to exit without saving
        
'''

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
    params['Gamma'] = 0
    params['H_min'] = 179
    params['H_max'] = 179
    params['S_min'] = 255
    params['S_max'] = 255
    params['V_min'] = 255
    params['V_max'] = 255
    params['Erode'] = 5
    params['Dilate'] = 5
    params['open:1 / close:0'] = 1
    params['Blur'] = 5

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
            if k != 'Gamma':
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
    

def checkParams(params):
    global colormodes
    if len(params.keys()) == len(colormodes):
        return True, None
    else:
        bools = np.array([i in params.keys() for i in colormodes])
        incomplete = colormodes[np.where(bools == False)]
        return False, incomplete
    

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

def createConf(params):
    low = np.array([params['H_min'],params['S_min'],params['V_min']])
    high = np.array([params['H_max'],params['S_max'],params['V_max']])
    conf = {'Gamma':params['Gamma'],'Erode':params['Erode'],'Dilate':params['Dilate'],'OC':params['open:1 / close:0'],'Blur':params['Blur'],'Low':low,'High':high}
    return conf

def run():
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
        for _ in xrange(params['Blur']):
            blur = cv2.bilateralFilter(blur,9,75,75)

        gamma = gamma_correct(blur,params['Gamma'])
        
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
        display(colorMode,displayMode,images,params['Gamma'])
        
        # Adding text to frame to represent current filtering mode.
        k = cv2.waitKey(1)


        if k == ord('<'):
            if displayMode == 0:
                displayMode = 4
            else:
                displayMode -= 1
        elif k == ord('>'):
            if displayMode == 4:
                displayMode = 0
            else:
                displayMode += 1

        elif k == ord('t'):
            colorMode = toggleMode(colorMode)
        elif k == ord('c'):
            color_conf[colorMode] = createConf(params)
        elif k == ord('p'):
            params['Gamma'] += 0.1
        elif k == ord('o'):
            params['Gamma'] -= 0.1

        elif k == ord('s'):
            ret, incomplete = checkParams(color_conf)
            if ret:
                cap.release()
                cv2.destroyAllWindows()
                return color_conf
            else:
                print('Color Configuration incomplete.')
                print('Please complete configuration for following colors: {}'\
                      .format(incomplete))
        elif k == 32:
            cap.release()
            cv2.destroyAllWindows()
            return None


