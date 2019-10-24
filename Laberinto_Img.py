import cv2
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pt
#import main

class Laberinto_Img():

    def __init__(self, ResolucionCamara = (1280, 720), NCasillasX = 7, NCasillasY = 7 ):
        self.sizeLab = []
        self.N1 = []
        self.N2 = []
        self.LocCas = []
        self.ResolucionCamara = ResolucionCamara
        self.NCasillasY = NCasillasY
        self.NCasillasX = NCasillasX
        self.camara = cv2.VideoCapture(0)
        self.camara.set(cv2.CAP_PROP_FRAME_WIDTH, self.ResolucionCamara[0])
        self.camara.set(cv2.CAP_PROP_FRAME_HEIGHT, self.ResolucionCamara[1])
        self.Laberinto = None
        self.HCasillas = 0
        self.WCasillas = 0
        self.Ubicaciones = {}
        self.cx = 0
        self.cy = 0
    
    def CapturarLaberinto(self):
        self.Laberinto = cv2.imread('img.jpg')
        # while(True):
        #     _,frame = self.camara.read()
        #     cv2.imshow('Capturando Laberinto...',frame)
        #     if cv2.waitKey(1) & 0xFF == ord('\r'):
        #         self.Laberinto = frame
        #         cv2.destroyAllWindows()
        #         break
        # ###cv2.imwrite('img.jpg', frame)
        # frame = None

    def RecortarLaberinto(self):
        nb_labels = 0
        self.Laberinto = cv2.cvtColor(self.Laberinto, cv2.COLOR_BGR2GRAY)
        while nb_labels != 3:
            n=10
            l = 256 
            im = ndimage.gaussian_filter(self.Laberinto, sigma=l/(4.*n))
            #im = self.Laberinto
            mask = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
            kernel = np.ones((7,7),np.uint8)
            dilatacion = cv2.dilate(mask,kernel,iterations = 2)

            nb_labels,label_im  = cv2.connectedComponents(dilatacion.astype(np.uint8))
            label_im2 = label_im * int(255/nb_labels)
            print(nb_labels)
            cv2.imshow("Dilatacion N de: {}".format(n), dilatacion.astype(np.uint8))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            cv2.imshow("Labeled N de: {}".format(n), label_im2.astype(np.uint8))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            if nb_labels != 3:
                cv2.imshow("Laberinto Editado", mask)
                self.CapturarLaberinto()
        a,b = np.shape(label_im)
        print(a)
        print(b)
        Flag = False
        for x in range(self.ResolucionCamara[0]-1):
            for y in range(self.ResolucionCamara[1]-1):
                if label_im[y][x] == 1:
                    self.N1 = [x,y]
                    Flag = True
                if Flag:
                    break
            if Flag:
                break
        Flag = False
        for x in range(self.ResolucionCamara[0]-1,-1,-1):
            for y in range(self.ResolucionCamara[1]-1,-1,-1):
                if label_im[y][x] == 2:
                    self.N2 = [x,y]
                    Flag = True
                if Flag:
                    break
            if Flag:
                break
        print(self.N1)
        print(self.N2)
        self.Laberinto = self.Laberinto[self.N1[1]:self.N2[1], self.N1[0]:self.N2[0]]
        self.MostrarLaberinto()
        self.__CalcularDimensiones()

    def __CalcularDimensiones(self):
        self.sizeLab = np.shape(self.Laberinto)
        self.WCasillas = round(self.sizeLab[1]/(self.NCasillasX))
        self.HCasillas = round(self.sizeLab[0]/(self.NCasillasY))
        for y in range(self.NCasillasY):
            for x in range(self.NCasillasX):
                numCasilla = str((x+1) + ((y)*(self.NCasillasY)))
                self.Ubicaciones[numCasilla] = [x*self.WCasillas, y*self.HCasillas, 
                                                (x+1)*self.WCasillas, (y+1)*self.HCasillas]
       
    def PruebaLabyCoor(self):
        print(self.Ubicaciones)
        Px = []
        Py = []
        for D in self.Ubicaciones.keys():
            Px.append(self.Ubicaciones[D][0])
            Py.append(self.Ubicaciones[D][1])
            Px.append(self.Ubicaciones[D][0])
            Py.append(self.Ubicaciones[D][3])
            Px.append(self.Ubicaciones[D][2])
            Py.append(self.Ubicaciones[D][1])
            Px.append(self.Ubicaciones[D][2])
            Py.append(self.Ubicaciones[D][3])
        plt.imshow(self.Laberinto)
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        plt.gca().invert_yaxis()
        plt.plot(Px,Py,"*b")
        plt.axis("off")

        EspaciosNegros = [6,9,10,11,13,16,18,22,23,25,26,27,32,37,38,39,41,42]
        for Espacio in EspaciosNegros:
            R = self.Ubicaciones[str(Espacio)]
            p = pt.Rectangle((R[0],R[1]), self.WCasillas,self.HCasillas, fill = True, color='black')
            ax.add_patch(p)
        plt.show()
        print("Area de Casilla: {}".format(self.WCasillas * self.HCasillas))

    def MostrarLaberinto(self):
        cv2.imshow("Laberinto Capturado", self.Laberinto)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def VideoLaberinto(self, EspaciosNegros, CasOrig, CasSig):
        while(True):
            _,frame = self.camara.read()
            frame = frame[self.N1[1]:self.N2[1], self.N1[0]:self.N2[0]]
            frameOrig = frame.copy()
            for Esp in EspaciosNegros:
                frame = cv2.rectangle(frame,(self.Ubicaciones[str(Esp)][0],self.Ubicaciones[str(Esp)][1]), 
                        (self.Ubicaciones[str(Esp)][2],self.Ubicaciones[str(Esp)][3]), (0,0,0),-1)
            cv2.imshow('Capturando Laberinto...',frame)
            self.BuscarRobot(frameOrig)
            if cv2.waitKey(1) & self.AccionRobot(frameOrig, CasOrig, CasSig):
                cv2.destroyAllWindows()
                break
        # self.camara.release()

    def BuscarRobot(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        n=10
        l = 256 
        im = ndimage.gaussian_filter(frame, sigma=l/(4.*n))
        mask = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
        kernel = np.ones((7,7),np.uint8)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        nb_labels,label_im  = cv2.connectedComponents(opening.astype(np.uint8))
        #label_im2 = label_im * int(255/nb_labels)
        if nb_labels!=2:
            return
        im8 = label_im.astype(np.uint8)
        #label_im2 = cv2.cvtColor(im8, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(im8, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        mayor_contorno = max(contours, key = cv2.contourArea)
        momentos = cv2.moments(mayor_contorno)
        cx = float(momentos['m10']/momentos['m00'])
        cy = float(momentos['m01']/momentos['m00'])
        if nb_labels!=2 and abs(cx-self.cx)<=10 and abs(cy-self.cy)<=10:
            return
        self.cx = cx
        self.cy = cy
        print("Centroide x: {}   Centroide y: {}".format(cx,cy))
        # cv2.imshow("Labeled", im8.astype(np.uint8))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def AccionRobot(self, frameOrig, CasOrig, CasSig):
        UO = self.Ubicaciones[str(CasOrig)]
        US = self.Ubicaciones[str(CasSig)]
        if UO[2]>self.cx>UO[0] and UO[3]>self.cy>UO[1]:
            print("En Casilla Actual")
            return False
        elif US[2]>self.cx>US[0] and US[3]>self.cy>US[1]:
            print("En Casilla siguiente")
            return True
        else:
            print("Sin Ubicacion")
            return False

# if __name__ == "__main__":
#     Lab = Laberinto_Img()
#     Lab.CapturarLaberinto()
#     Lab.MostrarLaberinto()
#     Lab.RecortarLaberinto()
#     CasSig = 8 
#     CasOrig = 15
#     EN = [6,9,10,11,13,16,18,22,23,25,26,27,32,37,38,39,41,42]
#     while CasOrig != CasSig:
#         Lab.VideoLaberinto(EN, CasOrig, CasSig)
    