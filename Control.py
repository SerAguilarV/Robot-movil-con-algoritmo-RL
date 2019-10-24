import time
import numpy as np
import cv2
from scipy import ndimage
import matplotlib.pyplot as plt

class Control():
    def __init__(self):
        self.imagen = []

    def GetImageCamera(self):
        cap = cv2.VideoCapture(0)
        while(True):
            ret,frame = cap.read()
            cv2.imshow('img1',frame)
            if cv2.waitKey(1) & 0xFF == ord('\r'): #save on pressing 'y' 
                cv2.destroyAllWindows()
                break
        cap.release()
        return self.__EnhacementImage(frame)

    def __EnhacementImage(self, img):
        self.__ShowImageUntilPress("Foto Utilizada", img)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        print(gray.shape)
        ret, imgf = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
        gray =  imgf 
        self.__ShowImageUntilPress("Foto Gris", gray)
        self.imagen = gray
        # edges = cv2.Canny(gray,50,150,apertureSize = 3)
        # kernel = np.ones((5,5), np.uint8)
        # edges = cv2.dilate(edges, kernel, iterations=4)
        # edges = cv2.erode(edges, kernel, iterations=4)
        # self.__ShowImageUntilPress("Foto Edges", edges)
        # minLineLength = 100
        # maxLineGap = 10
        # cont = 0
        # lines = cv2.HoughLinesP(edges,1,np.pi/180,50,minLineLength,maxLineGap)
        # for line in lines:
        #     x1,y1,x2,y2 = line[0]
        #     if x1<=20 or x1>=620:
        #         continue
        #     cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        #     cont +=1
        
        
        # lines = cv2.HoughLines(edges,1,np.pi/180,100)
        # cont = 0
        # print(lines)
        # for rho,theta in lines[0]:
        #     a = np.cos(theta)
        #     b = np.sin(theta)
        #     x0 = a*rho
        #     y0 = b*rho
        #     x1 = int(x0 + 1000*(-b))
        #     y1 = int(y0 + 1000*(a))
        #     x2 = int(x0 - 1000*(-b))
        #     y2 = int(y0 - 1000*(a))
        #     cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
        #     cont+=1
        #print(cont)
        #self.__ShowImageUntilPress("Foto con bordes", img)
    
    def __ShowImageUntilPress(self, message, img):
        while True:
            cv2.imshow(message, img)
            if cv2.waitKey(1) & 0xFF == ord('\r'): #save on pressing 'y' 
                cv2.destroyAllWindows()
                break

if __name__ == "__main__":
    control = Control()
    control.GetImageCamera()
    n = 10
    l = 256
    im = ndimage.gaussian_filter(control.imagen, sigma=l/(4.*n))
    mask = im > im.mean()

    label_im, nb_labels = ndimage.label(mask)
    print(nb_labels)
    plt.figure(figsize=(9,3))

    plt.subplot(121)
    plt.imshow(mask, cmap=plt.cm.gray)
    plt.axis('off')

    plt.subplot(122)
    plt.imshow(label_im, cmap=plt.cm.viridis)

    print(label_im)

    plt.axis('off')
    plt.subplots_adjust(wspace=0.02, hspace=0.02, top=1, bottom=0, left=0, right=1)
    plt.show()