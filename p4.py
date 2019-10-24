import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import time

cap = cv2.VideoCapture(1)
while(True):
    _,frame = cap.read()
    cv2.imshow('img1',frame)
    if cv2.waitKey(1) & 0xFF == ord('\r'): #save on pressing 'y' 
        cv2.destroyAllWindows()
        break

plt.imshow(frame)
pts = plt.ginput(1, timeout=-1)
plt.close()

cx = pts[0][0]
cy = pts[0][1]
#Convertimos la imagen a gris para poder introducirla en el bucle principal
frame_anterior = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
frame = frame_anterior
#Convertimos el punto elegido a un array de numpy que se pueda pasar como parametro
#a la funcion cv2.calcOpticalFlowPyrLK()
punto_elegido = np.array([[[cx,cy]]],np.float32)
print(punto_elegido)
 

lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
  
while(1):
    #Capturamos una imagen y la convertimos de RGB -> GRIS
    _,imagen = cap.read()
    time.sleep(0.1)
    frame_gray = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
 
    #Se aplica el metodo de Lucas Kanade
    punto_elegido, st, err = cv2.calcOpticalFlowPyrLK(frame_anterior, frame_gray, punto_elegido, None, **lk_params) 
    #Pintamos el centro (lo hacemos con un bucle por si, por alguna razon, decidimos pintar mas puntos)
    for i in punto_elegido:
          cv2.circle(imagen,tuple(i[0]), 3, (0,0,255), -1)
 
    #Se guarda el frame de la iteracion anterior del bucle
    frame_anterior = frame_gray.copy()
      
    #Mostramos la imagen original con la marca del centro
    cv2.imshow('Camara', imagen)
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break
  
cv2.destroyAllWindows()