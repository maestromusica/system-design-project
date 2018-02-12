import cv2
import numpy as np

cap = cv2.VideoCapture(0)
def gamma_correct(img,gamma):
    img = img/255.0
    img = cv2.pow(img,gamma)
    return np.uint8(img*255)
gamma = 0
while True:
    ret, frame = cap.read()
#    frame = cv2.imread('images/objects4.png')
    processed = gamma_correct(frame,27.4)
    gray = cv2.cvtColor(processed,cv2.COLOR_BGR2GRAY)
    cv2.putText(processed,str(gamma),(5,20),cv2.FONT_HERSHEY_COMPLEX,1,(200,200,200),2)
    cv2.imshow('gamma_correction',processed)
    cv2.imshow('gray',gray)
    k = cv2.waitKey(1)
    if k == 32:
        break
    elif k == ord('>'):
        gamma = gamma + 0.1
    elif k == ord('<'):
        gamma = gamma - 0.1

cv2.destroyAllWindows()
    
