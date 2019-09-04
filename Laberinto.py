import matplotlib.pyplot as plt
import numpy as np
import sys

class Laberinto():

    def __init__(self,filas = 8, columnas = 8):
        self.tamaño = (filas, columnas)
        
    def Obtener_Laberinto(self):
        pass

    def Dibujar_Laberinto(self):
        x = list(range(self.tamaño[0]))
        y = list(range(self.tamaño[1]))
        for i in x:
            for j in y:
                plt.plot(i, j, '*r')
        plt.show()


L = Laberinto()
L.Dibujar_Laberinto()
