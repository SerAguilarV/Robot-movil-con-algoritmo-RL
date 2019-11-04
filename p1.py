import cv2
import numpy as np
A = [5,2,5,7]
CA = 5
CS = 10
CX = 90
CY = 150
Mov = "Izquierda"

def CrearImagen(y, x, frame):
        x = abs(int(x))
        y = abs(int(y))
        Ima = np.zeros((y,300,3), np.uint8)
        hcat = cv2.hconcat((frame, Ima))
        font = cv2.FONT_HERSHEY_SIMPLEX
        textos = ["Centroide  X:{}  Y:{}".format(CX,CY),
                "Casilla Actual:{}  Casilla Siguiente:{}".format(CA,CS),
                "Direccion de Movimiento: {}".format(Mov),
                "Distacias: " ,
                "Arriba: {}     Abajo: {}".format(A[0],A[1]),
                "Derecha: {}     Izquierda: {}\n".format(A[2],A[3])]
        for i, texto in enumerate(textos):
            cv2.putText(hcat, texto, (x + 5, 20*(i+1)+30) , font ,0.4, (255,255,255))
        return hcat

camara = cv2.VideoCapture(0)
while(True):
    _,frame = camara.read()
    frameM = CrearImagen(480,640, frame.copy())
    cv2.imshow('Capturando Laberinto...',frameM)
    if cv2.waitKey(1) & 0xFF == ord('\r'):
        cv2.destroyWindow('Capturando Laberinto...')
        break
