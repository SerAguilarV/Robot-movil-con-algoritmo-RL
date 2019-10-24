import pygame
from pygame.locals import *
import sys
import numpy as np
import matplotlib.pyplot as plt
import math
from Laberinto_Img import Laberinto_Img

ImgLab = None

def main(NumeroEpisodios, Laberinto, RL, ImgLab):
    frames=1
    alpha=0.9
    gamma=0.95
    
    reco1= 	[[0, 	0, 	-1, 	0],	[0, 	0, 	-1, 	-1],    	[-1, 	0, 	0, 	-1],             [-1, 	-1, 	0, 	0],             [-1, 	-1, 	0, 	0],             [-1, 	-1, 	0, 	0],           [0, 	-1, 	0, 	-1],         [0, 	0, 	-1, 	-1],            [-1, 	0, 	-1, 	0],            [-1, 	-1, 	0, 	0],            [0, 	-1, 	-1, 	-1],             [0, 	0, 	-1, 	-1],             [0, 	-1, 	-1, 	0],           [-1, 	-1, 	0, 	0],             [-1, 	0, 	0, 	-1],             [0, 	0, 	-1, 	-1],             [-1, 	-1, 	-1, 	0],           [-1, 	-1, 	0, 	0],             [-1, 	-1, 	0, 	0],             [-1, 	-1, 	0, 	0],             [-1, 	0, 	-1, 	0],             [0, 	0, 	-1, 	-1],             [-1, 	0, 	0, 	-1],             [-1, 	-1, 	0, 	0],             [0, 	-1, 	-1, 	0],             [0, 	0, 	-1, 	-1],            [0, 	0, 	0, 	-1],            [0, 	0, 	-1, 	-1],          [0, 	0, 	0, 	-1],            [10, 	-1, 	0, 	0],            [0, 	10, 	0, 	0]]
    lab_q_1 = [[0,  0,  0,   0,  0,   0,   0,   0, 0],        [0,  3,  4,   5,  6,   7,   0,  29, 0],        [0,  2,  0,   0,  0,   8,   0,  28, 0],        [0,  1,  0,  27,  0,   9,  10,  11, 0],        [0,  0,  0,  26,  0,   0,   0,  12, 0],        [0, 23, 24,  25,  0,  15,  14,  13, 0],        [0, 22,  0,   0,  0,  16,   0,   0, 0],        [0, 21,  20, 19,  18, 17,  30,  31, 0],        [0,  0,  0,   0,  0,   0,   0,   0, 0]]

    reco2= [[0, 0,   0,  -10],      [0,    0,  -10, -10],               [0,    0,  -10, -10],             [ -100,  0,  -10, -10],               [ -10,  0,  -10, -10],               [ -10,  0,  -10, -10],               [ -10,  0,  -10, 0],               [ -100,  -10, 0,  -10],               [ -10,  -10, -100, -10],               [ -10,  -10, -10, -10],               [ -10,  -10,  -10, 0],               [ -100,  -100, 0,  -10],               [ -10,  -10, -100, -10],               [ -10,  -10, -10, -10],               [ -10,  -10, -10, 0],               [ -100,  -100, 0,  -10],            [ -10,  -10, -100, -10],     [ -10,  -10, -10, -10],            [ -10,  -10, -10, 0],           [ -100,  -100, 0,  -10],               [ -10,  -10, -100, -10],             [ -10,  -10, -10, -10],               [ -10,  -10, -10, 0],             [ -100,  -100, 0,  -10],        [ -10,  -10, -100, -10],               [ -10,  -10, -10, -10],              [-10,    -10, -10, 0],               [ 0,  -10,  -10, 0],        [0,    -10, -10, -10],        [0,    -10, -10, -10],      [0,    -100, -10, -10],         [0,    0,  -10, -10],      [0,    0,  100,  -10],               [0,    0,  100,  100]]
    lab_q_2 =[[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 34, 0], [0, 2, 0, 0, 0, 0, 0,33, 0], [0, 3, 0, 0, 0, 0, 0,32, 0], [0, 4, 8, 12, 16, 20, 24, 31], [0, 5, 9, 13, 17, 21, 25, 30, 0], [0, 6, 10, 14, 18, 22, 26, 29, 0], [0, 7, 11, 15, 19, 23, 27, 28, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    reco3=[[  -1,    0,    0,   -1],[  -1,   -1,    0,   -1],[  -1,   -1,    0,   -1],[  -1,   -1,    0,   -1],[  -1,   -1,    0,   -1],[  -1,   -1,    0,  10],[   0,   -1,    0,   -1],[  -1,    0,   -1,   -1],[  -1,   -1,   -1,   -1],[  -1,   -1,   -1,   -1],[  -1,   -1,   -1,   -1],[ 10,   -1,   -1, -10],[  -1,   -1,   -1,   -1],[   0,  10,   -1,   -1],[  -1,    0,   -1,   -1],[  -1,   -1,   -1,   -1],[  -1,   -1,   -1,   -1],[-10,   -1,   -1, -10],[  -1,   -1,   -1,   -1],[  -1, -10,  10,   -1],[   0,   -1,   -1,   -1],[  -1,    0,   -1,   -1],[  -1,   -1,   -1,   -1],[-10,   -1,   -1, -10],[  -1,   -1,   -1,   -1],[  -1, -10, -10,   -1],[  -1,   -1,   -1,   -1],[   0,   -1,   -1,   -1],[  -1,    0,   -1,   -1],[-10,   -1,   -1, -10],[  -1,   -1,   -1,   -1],[  -1, -10, -10,   -1],[  -1,   -1,   -1,   -1],[  -1,   -1,   -1,   -1],[   0,   -1,   -1,   -1],[-10,    0,   -1,   -1],[  -1,   -1,   -1,   -1],[  -1, -10, -10,   -1],[  -1,   -1,   -1,   -1],[  -1,   -1,   -1,   -1],[  -1,   -1,   -1,   -1],[   0,   -1,   -1,   -1],[  -1,    0,   -1,    0],[  -1,   -1, -10,    0],[  -1,   -1,   -1,    0],[  -1,   -1,   -1,    0],[  -1,   -1,   -1,    0],[  -1,   -1,   -1,    0],[   0,   -1,   -1,    0]]
    lab_q_3 =[[ 0,  0,  0,  0,  0,  0,  0,  0,  0], [ 0,  1,  2,  3,  4,  5,  6,  7,  0], [ 0,  8,  9, 10, 11, 12, 13, 14,  0], [ 0, 15, 16, 17, 18, 19, 20, 21,  0], [ 0, 22, 23, 24, 25, 26, 27, 28,  0], [ 0, 29, 30, 31, 32, 33, 34, 35,  0], [ 0, 36, 37, 38, 39, 40, 41, 42,  0], [ 0, 43, 44, 45, 46, 47, 48, 49,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0]]

    politica='Boltzmann'

    if Laberinto == 1:
        reco=reco1
        lab_q=lab_q_1
        EstadoObjetivo = 31
        Q=np.zeros([len(reco),4])
        #Q = -np.random.random([len(reco),4])/100
        EstadosIniciales=[1,1,1]
        Ima_Laberinto = 'laberinto1.png'

    elif Laberinto == 2:
        reco=reco2
        lab_q=lab_q_2
        EstadoObjetivo = 34
        #Q = np.random.random([len(reco),4])/100
        Q=np.zeros([len(reco),4])
        EstadosIniciales=[1,1,1]
        Ima_Laberinto = 'laberinto2.png'

    elif Laberinto == 3:
        reco=reco3
        lab_q=lab_q_3
        EstadoObjetivo = 13
        Q = np.random.random([len(reco),4])/100
        EstadosIniciales=[43,43,43]
        Ima_Laberinto = 'laberinto3.png'

    else:
        print("Laberinto Predeterminado")
        sys.exit()

    Pasos = 0
    contadorPasos= np.zeros([NumeroEpisodios])

    EstadoActual=-1
    Inicio_Episodio=True
    episodios=0

    WHITE = (255, 255, 255)
   
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    screen.fill(WHITE)
    personaje = pygame.image.load('robot.png')
    if RL==1:
        pygame.display.set_caption('Laberinto ' + str(Laberinto) + ' resuelto con Q-Learning-' + politica )
    elif RL==2:
        pygame.display.set_caption('Laberinto ' + str(Laberinto) + ' resuelto con SARSA-' + politica )
    elif RL==3:
        pygame.display.set_caption('Laberinto ' + str(Laberinto) + ' resuelto con BQ-' + politica )
    fondo=pygame.image.load(Ima_Laberinto)
    screen.blit(fondo,(25,25))
    pygame.display.update()
    clock = pygame.time.Clock()
    
    
    while True:
#===========================================================================================================
        if RL == 1:
            clock.tick(frames)
            if Inicio_Episodio==True:
                Recompensa=0
                Pasos=0
                Dir=np.random.randint(0, len(EstadosIniciales))
                EstadoActual=EstadosIniciales[Dir]
                y,x=Posicion_Estado(lab_q,EstadoActual)
                Inicio_Episodio=False
            else:
                AccionPosible=Selec_Accion_Boltzmann(EstadoActual,reco,Q,x,y,lab_q)
                Recompensa=reco[EstadoActual-1][AccionPosible]
                EstadoSiguiente,x,y = Selec_Estado(AccionPosible,y,x,lab_q)
                MoverRobot(EstadoActual, EstadoSiguiente, ImgLab, lab_q)
                Edo=EstadoActual-1
                EdoSig=EstadoSiguiente-1
                MaximoEdoSig=MaxEdoSig(EdoSig,Q,reco)
                #Actualizacion=Q[Edo][AccionPosible]
                Q[Edo][AccionPosible] = Q[Edo][AccionPosible]+alpha*(Recompensa+gamma*MaximoEdoSig-Q[Edo][AccionPosible])
                #Actualizacion=Q[Edo][AccionPosible]-Actualizacion
                EstadoActual=EstadoSiguiente
                Pasos+=1
#=====================================================================================================================
        elif RL == 2 or RL==3:
            clock.tick(frames)
            if Inicio_Episodio==True:
                if RL==3:
                    S=[]
                    A=[]
                    R=[]
                    S2=[]
                    A2=[]
                Recompensa=0
                Pasos=0
                Dir=np.random.randint(0, len(EstadosIniciales))
                EstadoActual=EstadosIniciales[Dir]
                y,x=Posicion_Estado(lab_q,EstadoActual)
                Inicio_Episodio=False
                AccionPosible=Selec_Accion_Boltzmann(EstadoActual,reco,Q,x,y,lab_q)           
            else:            
                Recompensa=reco[EstadoActual-1][AccionPosible]
                EstadoSiguiente,x,y = Selec_Estado(AccionPosible,y,x,lab_q)
                AccionSiguiente=Selec_Accion_Boltzmann(EstadoSiguiente,reco,Q,x,y,lab_q)
                MoverRobot(EstadoActual, EstadoSiguiente, ImgLab, lab_q)
                Edo=EstadoActual-1
                EdoSig=EstadoSiguiente-1
                #Ganancia=Q[Edo][AccionPosible]
                Q[Edo][AccionPosible] = Q[Edo][AccionPosible]+alpha*(Recompensa+gamma*(Q[EdoSig][AccionSiguiente])-Q[Edo][AccionPosible])
                #Ganancia=Q[Edo][AccionPosible]-Ganancia
                if RL==3:
                    S.append(EstadoActual)
                    A.append(AccionPosible)
                    R.append(Recompensa)
                    S2.append(EstadoSiguiente)
                EstadoActual=EstadoSiguiente
                AccionPosible=AccionSiguiente
                Pasos = Pasos + 1            

#==========================================================================================================
        personaje_x = 25+(x)*50
        personaje_y = 25+(y)*50
        screen.blit(fondo,(25,25))
        screen.blit(personaje, (personaje_x, personaje_y))
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    print(Q)
                    pygame.display.quit()
                    sys.exit()
                elif event.key == K_DOWN:
                    frames=1
                    print(Q)
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
                    
        pygame.display.flip()

        if Laberinto==2:
            m=-100
        else:
            m=-10    
        if Recompensa==m:
            Inicio_Episodio=True
            print(episodios)
            contadorPasos[episodios]=Pasos
            episodios=episodios+1
            if RL==3:
                for j in range(len(R)):
                    i=j+1
                    EstadoActual=S[-i]
                    AccionPosible=A[-i]
                    Recompensa=R[-i]
                    EstadoSiguiente=S2[-i]
                    Edo=EstadoActual-1
                    EdoSig=EstadoSiguiente-1
                    MaximoEdoSig=MaxEdoSig(EdoSig,Q,reco)
                    Q[Edo][AccionPosible] = Q[Edo][AccionPosible]+0.5*(Recompensa+0.95*MaximoEdoSig-Q[Edo][AccionPosible])

            if episodios==NumeroEpisodios:
                pygame.display.quit()
                B=np.ones(len(contadorPasos))
                B=B*contadorPasos
                return(B)
            
        
        if EstadoActual==EstadoObjetivo:
            Inicio_Episodio=True
            print(episodios)
            print(NumeroEpisodios)
            contadorPasos[episodios]=Pasos
            episodios=episodios+1
            if RL==3:
                for j in range(len(R)):
                    i=j+1
                    EstadoActual=S[-i]
                    AccionPosible=A[-i]
                    Recompensa=R[-i]
                    EstadoSiguiente=S2[-i]
                    Edo=EstadoActual-1
                    EdoSig=EstadoSiguiente-1
                    MaximoEdoSig=MaxEdoSig(EdoSig,Q,reco)
                    Q[Edo][AccionPosible] = Q[Edo][AccionPosible]+0.5*(Recompensa+0.95*MaximoEdoSig-Q[Edo][AccionPosible])
                                          
            if episodios==NumeroEpisodios:
                pygame.display.quit()
                B=np.ones(len(contadorPasos))
                B=B*contadorPasos
                return(B)

def MaxEdoSig(EdoSig,Q,reco):
    vec=reco[EdoSig][:]
    Maxim=[]
    r=0
    for i in range(len(vec)):
        if vec[i]==0:
            Maxim.append(-math.inf)
        else:
            Maxim.append(Q[EdoSig][i])
    return(max(Maxim))

def Selec_Accion_Greedy(EstadoActual,reco,Q):
    desiciones=[]
    direc=[]    
    for i in range(len(Q[EstadoActual-1][:])):
        if reco[EstadoActual-1][i]!=0:
            desiciones.append(Q[EstadoActual-1][i])
            direc.append(i)
    if len(direc)==1:
        return(direc[0])
    maxim=max(desiciones)
    flag=0
    a=0
    indice_max=0
    for i in desiciones:
        if i == maxim:
            flag+=1
            indice_max=a
        a+=1
    if flag==1:
        return direc[indice_max]
    else:
        val=np.random.randint(0,len(direc))
        return direc[val]

def Selec_Accion_Softmax(EstadoActual,reco,Q,x,y,lab_q):
    desiciones=[]
    direc=[]    
    for i in range(len(Q[EstadoActual-1][:])):
        if reco[EstadoActual-1][i]!=0:
            desiciones.append(Q[EstadoActual-1][i])
            direc.append(i)
    if len(direc)==1:
        return(direc[0])
    try:
        desiciones_exp = [math.exp(i/100) for i in desiciones]
    except:
        sys.exit()
    sum_desiciones_exp = sum(desiciones_exp)
    softmax = [i/sum_desiciones_exp for i in desiciones_exp]
    Valor=max(softmax)
    Valor2=softmax.index(Valor)
    Accion=direc[Valor2]
    return Accion

def Selec_Accion_Boltzmann(EstadoActual,reco,Q,x,y,lab_q):
    Valores=[]
    direc=[]    
    for i in range(len(Q[EstadoActual-1][:])):
        if reco[EstadoActual-1][i]!=0:
            Valores.append(Q[EstadoActual-1][i])
            direc.append(i)

    if len(direc)==1:
        return(direc[0])

    EstadosProb=[]
    for i in range(len(direc)):
        Estado,l,m=Selec_Estado(direc[i],y,x, lab_q)
        Val=[]
        for f in range(len(Q[EstadoActual-1][:])):
            Estado2,n,o=Selec_Estado(l,m,l,lab_q)
            if reco[Estado-1][f]!=0:
                Val.append(Q[Estado-1][f])
        if len(Val) == 0:
            EstadosProb.append(-math.inf)
            continue
        Vec=[math.exp((f)/1000) for f in Val]
        Vec_sum=sum(Vec)
        Vec2=[f for f in Vec]
        Vmax=(1/max(Vec2))*Valores[i]
        EstadosProb.append(Vmax)
    MaxEdoProb = max(EstadosProb)

    flag=0
    for i in range(len(EstadosProb)):
        if MaxEdoProb == EstadosProb[i]:
            flag+=1    
    if flag == 1:
        Valor2=EstadosProb.index(MaxEdoProb)
    else:
        Valor2=np.random.randint(0,len(EstadosProb))
    Accion=direc[Valor2]

    return Accion

def Selec_Estado(AccionPosible,y,x, lab_q):
    if AccionPosible == 0:
        x+=1
    elif AccionPosible ==1:
        x-=1
    elif AccionPosible ==2:
        y-=1
    else:
        y+=1

    Estado=lab_q[y][x]

    return(Estado,x,y)
        
def Posicion_Estado(lab_q,EstadoActual):
    Var_Temp=0;
    for fil in range(len(lab_q[:][0])):
        for col in range(len(lab_q[0][:])):
            if EstadoActual==lab_q[fil][col]:
                Var_Temp=1
                x=fil
                y=col
                break
        if Var_Temp==1:
            break
    return(x,y)

def Ploter_Grafica(GRAF,li,ls,R,L):
    X = np.arange(len(GRAF[0][:]))           
    ALG = ("Q-Learning","SARSA","Backward Q-Learning")
    POL = ("-Greedy","-Softmax","-Boltzmann")
    
    for i in range(3):
        plt.subplot(3,1,i+1)
        plt.bar(X,GRAF[i])
        plt.title("Promedio de Pasos con Politica "+ ALG[R] + POL[i] + "  Laberinto: " + str(L))
        plt.grid(True)
        plt.ylim(li,ls)
    plt.tight_layout()
    plt.show()

def MoverRobot(EdoAnt, EdoSig, ImgLab, Laberinto):
    L = np.array(Laberinto)[1:-1,1:-1]
    EN = [6,9,10,11,13,16,18,22,23,25,26,27,32,37,38,39,41,42]
    EdoAntN, EdoSigN = Reubicar(EdoAnt, EdoSig, L)
    ImgLab.VideoLaberinto(EN, EdoAntN, EdoSigN)

def Reubicar(EdoAnt, EdoSig, Laberinto):
    flag = False
    for y in range(len(Laberinto[:][0])):
        for x in range(len(Laberinto[:][0])):
            if EdoAnt == Laberinto[y][x]:
                flag = True
                break
        if flag:
            break
    EdoAntN = (x+1) + ((y)*(7))
    flag = False
    for y in range(len(Laberinto[:][0])):
        for x in range(len(Laberinto[:][0])):
            if EdoSig == Laberinto[y][x]:
                flag = True
                break
        if flag:
            break
    EdoSigN = (x+1) + ((y)*(7))
    return EdoAntN, EdoSigN

def Iniciar(NumeroEpisodios, Laberinto, RL):
    global ImgLab
    ImgLab = Laberinto_Img()
    ImgLab.CapturarLaberinto()
    ImgLab.MostrarLaberinto()
    ImgLab.RecortarLaberinto()
    main(NumeroEpisodios, Laberinto, RL, ImgLab)
            