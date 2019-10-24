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

def AccionesPygames(frames):            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:               
                pygame.display.quit()
                sys.exit()
            elif event.key == K_DOWN:
                frames=1
            elif event.key == K_UP:
                frames=60
            elif event.key == K_RIGHT:
                frames+=5
                if frames>=60:
                    frames==60
            elif event.key == K_LEFT:
                frames-=5
                if frames<=1:
                    frames==1
            elif event.key == K_SPACE:
                input()

def MoverRobot(fondo, personaje, x, y):
    personaje_x = 75+(x)*50
    personaje_y = 75+(y)*50
    screen.blit(fondo,(25,25))
    screen.blit(personaje, (personaje_x, personaje_y))

def FeaturesLab(L,EN,R,E,):
    TextRL = {1 : "Q-Learning", 2: "SARSA", 3:"Backward Q-Learning"}
    TextLab = {1 : "laberinto1.png", 2: "laberinto2.png", 3:"Laberinto1.png", 4:"Laberinto.png"}
    CasFin = 49 
    CasOrig = 15
    return CasOrig, CasFin, TextRL[R], TextLab[L]

def IniciarPygame(L, TextRL, TextLab, frames):
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    screen.fill( (255, 255, 255) )
    personaje = pygame.image.load('robot.png')
    pygame.display.set_caption('Laberinto ' + str(L) + ' resuelto' + TextRL )
    fondo=pygame.image.load(TextLab)
    screen.blit(fondo,(25,25))
    pygame.display.update()
    clock = pygame.time.Clock()
    clock.tick(frames)
    return fondo, screen, personaje, clock

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
    CasOrig, CasFin, TextRL, TextLab = FeaturesLab(L,EN,R,E)
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    screen.fill( (255, 255, 255) )
    personaje = pygame.image.load('robot.png')
    pygame.display.set_caption('Laberinto ' + str(L) + ' resuelto' + TextRL )
    fondo=pygame.image.load(TextLab)
    screen.blit(fondo,(25,25))
    pygame.display.update()
    clock = pygame.time.Clock()
    clock.tick(2)
    #fondo, screen, personaje, clock = IniciarPygame(L, TextRL, TextLab, 2)
    RobotOm = Robot(CasOrig = CasOrig, CasMeta=CasFin, EdoNegro = EN)
    for Repeticion in range(E):
        CasAnt = CasOrig
        RobotOm.EstadoActual = CasAnt
        X,Y = RobotOm.ObtenerCoordenadas(CasAnt)
        MoverRobot(fondo, personaje, X, Y)
        AccionesPygames(2)
        pygame.display.flip()
        steps = 1
        while CasAnt != CasFin:
            CasAnt, Accion = RobotOm.SeleccionarAccion()
            Reco = RobotOm.ObtenerRecompensa(CasAnt, Accion)
            CasSig = RobotOm.MoverRobotSigCasilla(CasAnt, Accion)
            RobotOm.ActualizacionQ(CasAnt, Accion, Reco, CasSig)
            # print("*"*30+"\nCasilla Anterior: {}\nAccion: {}\nCasilla Siguiente: {}\nRecompensa: {}".format(\
            #             CasAnt, Accion, CasSig, Reco))
            CasAnt = CasSig
            X,Y = RobotOm.ObtenerCoordenadas(CasAnt)
            MoverRobot(fondo, personaje, X, Y)
            AccionesPygames(2)
            pygame.display.flip()
            steps +=1
        print("Episodio {} se termino, se dieron {} pasos".format(Repeticion, steps))