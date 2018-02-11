import cv2
import numpy as np

cap = cv2.VideoCapture(0)
detector = cv2.SimpleBlobDetector_create()

while True:
    ret, frame = cap.read()
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    keypoints = detector.detect(img)
    img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow("Keypoints", img_with_keypoints)
    k = cv2.waitKey(0)
    if k == 32:
        break

cap.release()
cv2.destroyAllWindows()
