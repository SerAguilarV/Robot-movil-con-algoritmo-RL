import socket
import json
from bson import json_util
import cv2
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pt
import time

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
                numCasilla = str((x+1) + ((y)*(self.NCasillasY)))
                self.Ubicaciones[numCasilla] = [x*self.WCasillas, y*self.HCasillas, 
                                                (x+1)*self.WCasillas, (y+1)*self.HCasillas]

    def MostrarLaberinto(self):
        cv2.imshow("Laberinto Capturado", self.Laberinto)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def Comenzar(self):
        f = plt.figure()
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

    def VideoLaberinto(self, CasOrig, CasSig):
        f = plt.figure()
        while(True):
            _,frame = self.camara.read()
            frame = frame[self.N1[1]:self.N2[1], self.N1[0]:self.N2[0]]
            frameOrig = frame.copy()
            for Esp in self.EspaciosNegros:
                frame = cv2.rectangle(frame,(self.Ubicaciones[str(Esp)][0],self.Ubicaciones[str(Esp)][1]), 
                        (self.Ubicaciones[str(Esp)][2],self.Ubicaciones[str(Esp)][3]), (0,0,0),-1)
            cv2.imshow('Capturando Laberinto...',frame)
            img, r = self.BuscarRobot(frameOrig)
            if cv2.waitKey(1) and not r:
                continue
            if cv2.waitKey(1) and self.AccionRobot(frameOrig, CasOrig, CasSig):
                cv2.destroyAllWindows()
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
            return None, False
        im8 = label_im.astype(np.uint8)
        #label_im2 = cv2.cvtColor(im8, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(im8, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        mayor_contorno = max(contours, key = cv2.contourArea)
        momentos = cv2.moments(mayor_contorno)
        cx = float(momentos['m10']/momentos['m00'])
        cy = float(momentos['m01']/momentos['m00'])
        # if abs(cx-self.cx)<=100 and abs(cy-self.cy)<=100:
        #     print("Sin Ubicacion, distanciado")
        #     return False
        self.cx = round(cx,2)
        self.cy = round(cy,2)
        return label_im2, True
        # cv2.imshow("Labeled", im8.astype(np.uint8))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def AccionRobot(self, frameOrig, CasOrig, CasSig):
        print("Centroide x: {}   Centroide y: {}".format(self.cx,self.cy))
        UO = self.Ubicaciones[str(CasOrig)]
        US = self.Ubicaciones[str(CasSig)]
        self.Dists = [round(self.cx - UO[0]), round(self.cy - UO[1]), 
                      round(UO[2] - self.cx), round(UO[3] - self.cy)]
        # DI = self.cy - UO[1]
        # DA = self.cy - UO[1]
        # DB = UO[3] - self.cy
        # DD = UO[2] - self.cx
        # print("Distancia Izquierda: {}".format(DI))
        # print("Distancia Arriba: {}".format(DA))
        # print("Distancia Abajo: {}".format(DB))
        # print("Distancia Derecha: {}".format(DD))
        if UO[2]>self.cx>UO[0] and UO[3]>self.cy>UO[1]:
            print("En Casilla Actual")
            return False
        elif US[2]>self.cx>US[0] and US[3]>self.cy>US[1]:
            print("En Casilla siguiente")
            self.EnviarDatosRobot(None,None)
            time.sleep(2)
            return True
        else:
            return False
    
    def ControlRobot(self, CasOrig, CasSig):
        Movimiento = self.__GetDireccion(CasOrig, CasSig)
        print(Movimiento)
        print(self.Dists)
        Velocidades = self.Velocidades(Movimiento)
        self.EnviarDatosRobot(Movimiento, Velocidades)

    def Velocidades(self, Movimiento):
        if Movimiento == "Arriba":
            post = {"0" : {"Sentido" : True, "Vel" : 0},
                "1" : {"Sentido" : True, "Vel" : 0},
                "2" : {"Sentido" : False, "Vel" : 0.5},
                "3" : {"Sentido" : True, "Vel" : 0.5}}
        elif Movimiento == "Abajo":
            post = {"0" : {"Sentido" : True, "Vel" : 0},
                "1" : {"Sentido" : True, "Vel" : 0},
                "2" : {"Sentido" : True, "Vel" : 0.5},
                "3" : {"Sentido" : False, "Vel" : 0.5}}
        elif Movimiento == "Derecha":
            post = {"0" : {"Sentido" : False, "Vel" : 0.5},
                "1" : {"Sentido" : True, "Vel" : 0.5},
                "2" : {"Sentido" : True, "Vel" : 0},
                "3" : {"Sentido" : True, "Vel" : 0}}
        elif Movimiento == "Izquierda":
            post = {"0" : {"Sentido" : True, "Vel" : 0.5},
                "1" : {"Sentido" : False, "Vel" : 0.5},
                "2" : {"Sentido" : True, "Vel" : 0},
                "3" : {"Sentido" : True, "Vel" : 0}}
        else:
            pass
        return post

    def __GetDireccion(self, CasOrig, CasSig):
        CorOrg = [] 
        CorSig = []
        self.sizeLab = np.shape(self.Laberinto)
        self.WCasillas = round(self.sizeLab[1]/self.NCasillasX)
        self.HCasillas = round(self.sizeLab[0]/self.NCasillasY)
        for y in range(self.NCasillasY):
            for x in range(self.NCasillasX):
                numCasilla = (x+1) + ((y)*(self.NCasillasY))
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
        post = {'Mensaje' : "Socket Conectado"}
        self.SocketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SocketObj.connect(('192.168.100.32', 10701))
        self.SocketObj.sendall(json.dumps(post, default=json_util.default).encode('utf-8'))
        respuesta = json.loads(self.SocketObj.recv(8192).decode('utf-8'))
        print(respuesta['Resp'])
        if respuesta['Resp'] == "ok":
            return

    def EnviarDatosRobot(self, Movimiento, Velocidades):
        if not self.SocketObj:
            self.CrearSocket()
        if Velocidades:
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
#     CasSig = 8 
#     CasOrig = 15
#     EN = [6,9,10,11,13,16,18,22,23,25,26,27,32,37,38,39,41,42]
#     while CasOrig != CasSig:
#         Lab.VideoLaberinto(EN, CasOrig, CasSig)
    