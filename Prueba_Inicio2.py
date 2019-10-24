import pygame
from pygame.locals import *
import sys
import numpy as np
import matplotlib.pyplot as plt
import math
import Laberinto_Img
from Laberinto_Img import Laberinto_Img
import Interfaz
from Robot import Robot
import time
from Prueba_Lab_Ant import Iniciar

if __name__ == "__main__":
    WinMain = Interfaz.WindowMain()
    L, EN, R, E  = WinMain.GetDatos()
    print("Laberinto: {}".format(L))
    print("Espcios en Negro: {}".format(EN))
    print("RL: {}".format(R))
    print("Episodios: {}".format(E))
    # LabImg = Laberinto_Img()
    # LabImg.CapturarLaberinto()
    # LabImg.MostrarLaberinto()
    # LabImg.RecortarLaberinto()
    # x = LabImg.sizeLab
    Iniciar(E, L, R)