import cv2 as cv
import numpy as np


cap = cv.VideoCapture(0)

while(cap.isOpened()):
    gray = cv.medianBlur(cv.cvtColor(cap.read()[1], cv.COLOR_BGR2GRAY),5)

    # -- detectMultiScale ? ---
    circles_img = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 40,
                            param1=50, param2=30, minRadius=0, maxRadius=0)
    circles_img = np.uint16(np.around(circles_img))
    
    for i in circles_img[0,:]:
        cv.circle(gray, (i[0],i[1]),i[2],(0,255,0),2)
        cv.circle(gray, (i[0],i[1]),2,(0,0,255),3)

    cv.imshow('Detected Circles',gray)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()