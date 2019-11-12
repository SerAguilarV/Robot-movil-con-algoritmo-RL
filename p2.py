import cv2
import numpy as np 
import matplotlib.pyplot as plt
from scipy import ndimage

camara = cv2.VideoCapture(0)
lk = dict(winSize = (15,15), maxLevel = 2, criteria = (cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,10,0.03))

def F1(camara):
    while True:
        _,frame1 = camara.read()
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2YUV)
        frame1[:,:,0] = cv2.equalizeHist(frame1[:,:,0])
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_YUV2BGR)
        frame = cv2.cvtColor(frame1.copy(), cv2.COLOR_BGR2HSV)
        umbral_bajo = (170, 100, 100)
        umbral_alto = (179, 255, 255)
        mask = cv2.inRange(frame,umbral_bajo, umbral_alto)

        umbral_bajo2 = (0, 100, 100)
        umbral_alto2 = (10, 255, 255)
        mask2 = cv2.inRange(frame,umbral_bajo2, umbral_alto2)

        mask = mask + mask2

        kernel = np.ones((7,7),np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)
        opening = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)
        n=10
        l = 256 
        im = ndimage.gaussian_filter(mask, sigma=l/(4.*n))

        contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            continue
        mayor_contorno = max(contours, key = cv2.contourArea)
        
        for i in mayor_contorno: 
            cv2.circle(frame1, tuple(i[0]),3, (0,0,255),-1)
        
        opening = cv2.cvtColor(opening,cv2.COLOR_GRAY2BGR)

        momentos = cv2.moments(mayor_contorno)
        cx = float(momentos['m10']/momentos['m00'])
        cy = float(momentos['m01']/momentos['m00'])
        cv2.circle(frame1, (int(cx),int(cy)), 10, (0,255,0), -1)
        print("Cx : {},  Cy:{}".format(cx,cy))
        hcat = cv2.hconcat((frame1, opening))
        #hcat = cv2.resize(hcat,(1000,350))
        cv2.imshow("img", hcat)
        if cv2.waitKey(1) & 0xFF == ord('\r'):
            cv2.destroyWindow('img')
            break

F1(camara)