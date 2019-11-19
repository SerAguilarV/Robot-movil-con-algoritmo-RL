import socket
import json
from bson import json_util
import cv2
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pt
import time
import math

Mov_Arr = [True, True, False, True]
Mov_Aba = [True, True, True, False]
Mov_Izq = [True, False, True, True]
Mov_Der = [False, True, True, True]
Vel_Lat = [1, 0.7, 0, 0]
Vel_Hor = [0, 0, 0.9, 0.9]

class Laberinto_Img():

    def __init__(self, EspaciosNegros, ResolucionCamara = (1280, 720), NCasillasX = 7, NCasillasY = 7 ):
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
        self.Dists = []
        self.SocketObj = None
        self.Clicks= []
        self.cont = 0
        self.EspaciosNegros = EspaciosNegros
        self.Movimiento = ""
        self.DataEnvi = {}
        self.Dsx = 0 
        self.Dsy = 0
    
    def ClicksFunction(self, event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print(x,y)
            self.Clicks.append([x,y])
            self.cont+=1

    def CapturarLaberinto(self):
        # self.Laberinto = cv2.imread('img.jpg')
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.ClicksFunction)
        while(True):
            _,self.Laberinto = self.camara.read()
            cv2.imshow('image',self.Laberinto)
            if cv2.waitKey(1) & 0xFF == ord('\r'):
                cv2.destroyAllWindows()
                break
            if self.cont ==2:
                cv2.destroyAllWindows()
                print(self.Clicks)
                break
        ###cv2.imwrite('img.jpg', frame)
        frame = None

    def RecortarLaberinto(self):
        self.N1 = self.Clicks[0]
        self.N2 = self.Clicks[1]
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
                numCasilla = str((x+1) + ((y)*(self.NCasillasX)))
                print(numCasilla)
                self.Ubicaciones[numCasilla] = [x*self.WCasillas, y*self.HCasillas, 
                                                (x+1)*self.WCasillas, (y+1)*self.HCasillas]

    def MostrarLaberinto(self):
        cv2.imshow("Laberinto Capturado", self.Laberinto)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def Comenzar(self):
        #f = plt.figure()
        while(True):
            _,frame = self.camara.read()
            frame = frame[self.N1[1]:self.N2[1], self.N1[0]:self.N2[0]]
            frameOrig = frame.copy()
            for Esp in self.EspaciosNegros:
                frame = cv2.rectangle(frame,(self.Ubicaciones[str(Esp)][0],self.Ubicaciones[str(Esp)][1]), 
                        (self.Ubicaciones[str(Esp)][2],self.Ubicaciones[str(Esp)][3]), (0,0,0),-1)
            cv2.imshow('Capturando Laberinto...',frame)
            if cv2.waitKey(1) & 0xFF == ord('\r'):
                cv2.destroyWindow('Capturando Laberinto...')
                break

    def CrearImagen(self, y, x, frame, CO, CS, img2):
        x = abs(int(x))
        y = abs(int(y))
        Ima = np.zeros((y,x,3), np.uint8)
        hcat = cv2.hconcat((frame, Ima))
        font = cv2.FONT_HERSHEY_SIMPLEX
        US = self.Ubicaciones[str(CS)]
        Dx = (US[2] + US[0])/2  
        Dy = (US[3] + US[1])/2
        d = np.sqrt((self.cx - Dx )**2 + (self.cy - Dy)**2)
        self.Dsx = round(Dx-self.cx,1)
        self.Dsy = round(Dy-self.cy,1)
        Post = self.Velocidades(self.Movimiento, [self.Dsx,self.Dsy])
        Iz =  Post["2"]["Vel"]
        De =  Post["3"]["Vel"]
        Arr =  Post["0"]["Vel"]
        Aba =  Post["1"]["Vel"]
        textos = ["Centroide  X:{}  Y:{}".format(int(self.cx), int(self.cy)),
                "Casilla Actual: {}  Casilla Siguiente: {}".format(CO,CS),
                "Direccion de Movimiento: {}".format(self.Movimiento),
                #"Distancias: " ,
                #"   Arriba: {}     Abajo: {}".format(self.Dists[1], self.Dists[3]),
                #"   Derecha: {}     Izquierda: {}".format(self.Dists[2],self.Dists[0]),
                "Movimiento de Llantas",
                "Iz:{} De:{} Arr:{} Aba:{}".format(Iz, De, Arr, Aba),
                "Distancia Eje X: {}".format(self.Dsx),
                "Distancia Eje Y: {}".format(self.Dsy)]
                # self.Dists = [ Izquierda , Arriba , Derecha, Abajo ]
        self.DataEnvi = {"Mov": self.Movimiento, "Dx": self.Dsx, "Dy" : self.Dsy}
        for i, texto in enumerate(textos):
            cv2.putText(hcat, texto, (x + 5, 50*(i+1)+10) , font ,1.2, (255,255,255))
        # W,H = self.__ResizeImagen(hcat.shape[0], hcat.shape[1])
        if not img2 is None: 
            hcat = cv2.resize(hcat,(int(img2.shape[1]),int(img2.shape[0])))
            vcat = cv2.vconcat((hcat, img2))
        else:
            vcat = hcat
        return vcat

    def VideoLaberinto(self, CasOrig, CasSig):
        #f = plt.figure()
        while True:
            _,frame = self.camara.read()
            frame = frame[self.N1[1]:self.N2[1], self.N1[0]:self.N2[0]]
            frameOrig = frame.copy()
            for Esp in self.EspaciosNegros:
                frame = cv2.rectangle(frame,(self.Ubicaciones[str(Esp)][0],self.Ubicaciones[str(Esp)][1]), 
                        (self.Ubicaciones[str(Esp)][2],self.Ubicaciones[str(Esp)][3]), (0,0,0),-1)
            
            img = self.BuscarRobot2(frameOrig)                            
            if cv2.waitKey(1) and img is None:
                self.EnviarDatosRobot("0", "0")
                continue
            else:
                R = self.AccionRobot(frameOrig, CasOrig, CasSig)
                self.CalcularMov(CasOrig, CasSig)
                frameM = self.CrearImagen(self.N1[1]-self.N2[1], self.N1[0]-self.N2[0], 
                                frame.copy(), CasOrig, CasSig, img)
                cv2.imshow('Capturando Laberinto...',frameM)
            if cv2.waitKey(1) and R:
                #cv2.destroyAllWindows()
                break
            else:
                self.ControlRobot(CasOrig, CasSig)

    def BuscarRobot(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        n=10
        l = 256 
        im = ndimage.gaussian_filter(frame, sigma=l/(4.*n))
        mask = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
        kernel = np.ones((5,5),np.uint8)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        nb_labels,label_im  = cv2.connectedComponents(opening.astype(np.uint8))
        label_im2 = label_im * int(255/nb_labels)
        if nb_labels!=2:
            print("Sin Ubicacion, Mas Objetos: {}".format(nb_labels))
            return None
        im8 = label_im.astype(np.uint8)
        #label_im2 = cv2.cvtColor(im8, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(im8, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        mayor_contorno = max(contours, key = cv2.contourArea)
        momentos = cv2.moments(mayor_contorno)
        cx = float(momentos['m10']/momentos['m00'])
        cy = float(momentos['m01']/momentos['m00'])
        # if abs(cx-self.cx)<=
        self.cx = round(cx,2)
        self.cy = round(cy,2)
        return label_im2

    def BuscarRobot2(self, frame1):
        # frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2YUV)
        # frame1[:,:,0] = cv2.equalizeHist(frame1[:,:,0])
        # frame1 = cv2.cvtColor(frame1, cv2.COLOR_YUV2BGR)
        frame = cv2.cvtColor(frame1.copy(), cv2.COLOR_BGR2HSV)
        umbral_bajo = (170, 100, 100)
        umbral_alto = (179, 255, 255)
        mask = cv2.inRange(frame,umbral_bajo, umbral_alto)
        umbral_bajo2 = (0, 100, 100)
        umbral_alto2 = (10, 255, 255)
        mask2 = cv2.inRange(frame,umbral_bajo2, umbral_alto2)
        mask = mask + mask2
        kernel = np.ones((7,7),np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        opening = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        n=10
        l = 256 
        im = ndimage.gaussian_filter(mask, sigma=l/(4.*n))
        contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        mayor_contorno = max(contours, key = cv2.contourArea)
        for i in mayor_contorno: 
            cv2.circle(frame1, tuple(i[0]),3, (0,0,255),-1)
        opening = cv2.cvtColor(opening,cv2.COLOR_GRAY2BGR)
        momentos = cv2.moments(mayor_contorno)
        self.cx = float(momentos['m10']/momentos['m00'])
        self.cy = float(momentos['m01']/momentos['m00'])
        cv2.circle(frame1, (int(self.cx),int(self.cy)), 10, (0,255,0), -1)
        #print("Cx : {},  Cy:{}".format(self.cx,self.cy))
        hcat = cv2.hconcat((frame1, opening))
        W,H = self.__ResizeImagen(frame1.shape[0], frame1.shape[1])
        hcat = cv2.resize(hcat,(int(W),int(H)))
        return hcat

    def __ResizeImagen(self, width, heigth):
        if width>heigth:
            nWidth = 300
            nHeigth = (heigth*nWidth)/(4*width)
        else:
            nHeigth = 300
            nWidth = (4*width*nHeigth)/heigth
        return nWidth, nHeigth

    def AccionRobot(self, frameOrig, CasOrig, CasSig):
        #print("Centroide x: {}   Centroide y: {}".format(self.cx,self.cy))
        UO = self.Ubicaciones[str(CasOrig)]
        US = self.Ubicaciones[str(CasSig)]
        self.Dists = [round(self.cx - UO[0]), round(self.cy - UO[1]), 
                      round(UO[2] - self.cx), round(UO[3] - self.cy)]
        # self.Dists = [ Izquierda , Arriba , Abajo, Derecha ]
        if UO[2]>self.cx>UO[0] and UO[3]>self.cy>UO[1]:
            #print("En Casilla Actual")
            return False
        elif 50+(US[2]+ US[0])/2 >self.cx> -50+(US[2]+ US[0])/2 \
                and 50+(US[3]+US[1])/2>self.cy>-50+(US[3]+US[1])/2:
            #print("En Casilla siguiente")
            self.EnviarDatosRobot(None,None)
            #time.sleep(2)
            return True
        else:
            return False

    def CalcularMov(self, CasOrig, CasSig):
        self.Movimiento = self.__GetDireccion(CasOrig, CasSig) 
        # print(self.Movimiento)
        # print(self.Dists)
    
    def ControlRobot(self, CasOrig, CasSig):
        Velocidades = self.Velocidades(self.Movimiento)
        print(Velocidades)
        self.EnviarDatosRobot(self.Movimiento, Velocidades)

    def Velocidades2(self, Movimiento, data = False):
        if Movimiento == "Arriba":
            S = [True, True, False, True]
            V = [0, 0, 1, 1]
        elif Movimiento == "Abajo":
            S = [True, True, True, False]
            V = [0, 0, 1, 1]
        elif Movimiento == "Derecha":
            S = [False, True, True, True]
            V = [1, 0.4, 0, 0]
        elif Movimiento == "Izquierda":
            S = [True, False, True, True]
            V = [0.4, 1, 0, 0]
        else:
            S = [True, True, True, True]
            V = [0, 0, 0, 0]
        return self.__crearPost(V, S)

    def Velocidades(self, Movimiento, data = False):
        ts = 0.1
        if not data:
            Dx = self.DataEnvi["Dx"]
            Dy = self.DataEnvi["Dy"]
        else:
            Dx = data[0] 
            Dy = data[1]
        nF = 15
        if Movimiento == "Arriba":
            if Dx>nF:
                P = self.__crearPost(Vel_Lat, Mov_Der)
                self.EnviarDatosRobot(Movimiento, P)
                time.sleep(ts)
                return self.__crearPost([0, 0,0.9,0.9], Mov_Arr)
            elif Dx<-nF:
                P = self.__crearPost(Vel_Lat, Mov_Izq)
                self.EnviarDatosRobot(Movimiento, P)
                time.sleep(ts)
                return self.__crearPost([0,0,0.9,0.9], Mov_Arr)
            else:
                return self.__crearPost(Vel_Hor, Mov_Arr)
                
        elif Movimiento == "Abajo":
            if Dx>nF:
                P = self.__crearPost(Vel_Lat, Mov_Der)
                self.EnviarDatosRobot(Movimiento, P)
                time.sleep(ts)
                return self.__crearPost([0,0,0.9,0.9], Mov_Aba)
            elif Dx<-nF:
                P = self.__crearPost(Vel_Lat, Mov_Izq)
                self.EnviarDatosRobot(Movimiento, P)
                time.sleep(ts)
                return self.__crearPost([0,0,0.9,0.9], Mov_Aba)
            else:
                return self.__crearPost(Vel_Hor, Mov_Aba)

        elif Movimiento == "Derecha":
            if Dy > nF:
                P = self.__crearPost(Vel_Hor, Mov_Aba)
                self.EnviarDatosRobot(Movimiento, P)
                time.sleep(ts)
                return self.__crearPost([0.9,0.6,0,0], Mov_Der)
            elif Dy < -nF:
                P = self.__crearPost(Vel_Hor, Mov_Arr)
                self.EnviarDatosRobot(Movimiento, P)
                time.sleep(ts)
                return self.__crearPost([0.9,0.7,0,0], Mov_Der)
            else:
                return self.__crearPost(Vel_Lat, Mov_Der)

        elif Movimiento == "Izquierda":
            S = [True, False, True, True]
            if Dy > nF:
                P = self.__crearPost(Vel_Hor, Mov_Aba)
                self.EnviarDatosRobot(Movimiento, P)
                time.sleep(ts)
                return self.__crearPost([0.9,0.6,0,0], Mov_Izq)
            elif Dy < -nF:
                P = self.__crearPost(Vel_Hor, Mov_Arr)
                self.EnviarDatosRobot(Movimiento, P)
                time.sleep(ts)
                return self.__crearPost([0.9,0.7,0,0], Mov_Izq)
            else:
                return self.__crearPost(Vel_Lat, Mov_Izq)

        else:
            S = [True, True, True, True]
            V = [0, 0, 0, 0]
            return self.__crearPost(V, S)

    def __crearPost(self,V,S):
        post = {"0" : {"Sentido" : S[0], "Vel" : V[0]},
                "1" : {"Sentido" : S[1], "Vel" : V[1]},
                "2" : {"Sentido" : S[2], "Vel" : V[2]},
                "3" : {"Sentido" : S[3], "Vel" : V[3]}}
        return post

    def __GetDireccion(self, CasOrig, CasSig):
        CorOrg = [] 
        CorSig = []
        self.sizeLab = np.shape(self.Laberinto)
        self.WCasillas = round(self.sizeLab[1]/self.NCasillasX)
        self.HCasillas = round(self.sizeLab[0]/self.NCasillasY)
        for y in range(self.NCasillasY):
            for x in range(self.NCasillasX):
                numCasilla = (x+1) + ((y)*(self.NCasillasX))
                if numCasilla == CasOrig:
                    CorOrg = [x,y]
                if numCasilla == CasSig:
                    CorSig = [x,y]
        
        if CorOrg[0] == CorSig[0]:
            if CorOrg[1] > CorSig[1]:
                return "Arriba"
            return "Abajo"
        elif CorOrg[1] == CorSig[1]:
            if CorOrg[0] > CorSig[0]:
                return "Izquierda"
            return "Derecha"

    def CrearSocket(self):
        while True:
            try:
                post = {'Mensaje' : "Socket Conectado"}
                self.SocketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.SocketObj.connect(('192.168.43.31', 10701))
                self.SocketObj.sendall(json.dumps(post, default=json_util.default).encode('utf-8'))
                respuesta = json.loads(self.SocketObj.recv(8192).decode('utf-8'))
                print(respuesta['Resp'])
                if respuesta['Resp'] == "ok":
                    return
            except:
                print("No contecta con la Rasberry")

    def EnviarDatosRobot(self, Movimiento, Velocidades):
        if not self.SocketObj:
            self.CrearSocket()
        if Velocidades == "0":
            post = {'Mensaje' : "Robot detenido, mejorando imagen" } 
        elif Velocidades:
            post = {'Mensaje' : Movimiento ,"Llantas":Velocidades, "Distancias":self.Dists} 
        else:
            post = {"Mensaje" : "Siguiente Casilla"}
        self.SocketObj.sendall(json.dumps(post, default=json_util.default).encode('utf-8'))
        respuesta = json.loads(self.SocketObj.recv(8192).decode('utf-8'))
        print(respuesta['Resp'])
        if respuesta['Resp'] == "ok":
            return
        # print("Llantas Laterales: {}\nLlantas Frontales: {}\nDistancias: {}"\
        #         .format(Laterales, Frontales, self.Dists))
        

# if __name__ == "__main__":
#     Lab = Laberinto_Img()
#     Lab.CrearSocket()
#     time.sleep(2)
#     Lab.EnviarDatosRobot(Movimiento="Arriba", Laterales=True, Frontales=True)
#     time.sleep(5)
#     Lab.EnviarDatosRobot(Movimiento="Abajo", Laterales=False, Frontales=True)
    # Lab.CapturarLaberinto()
    # Lab.MostrarLaberinto()
    # Lab.RecortarLaberinto()
    # ImgLab.Comenzar()
#     CasSig = 8 
#     CasOrig = 15
#     EN = [6,9,10,11,13,16,18,22,23,25,26,27,32,37,38,39,41,42]
#     while CasOrig != CasSig:
#         Lab.VideoLaberinto(EN, CasOrig, CasSig)
    