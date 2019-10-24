import numpy as np
import math

class Robot():
    def __init__(self, CasOrig, CasMeta, EdoNegro = [], SizeLab = [7,7]):
        self.EdoNegro = EdoNegro
        self.SizeLab = SizeLab
        self.EstadoActual =  CasOrig
        self.EstadoMeta = CasMeta
        self.LabMat = self.__CrearMatrizLab()
        self.MatReco = self.__CrearMatrizReco()
        self.Recompensa=0
        self.Pasos=0
        self.EstadoActual=CasOrig
        self.MatrizQ = np.zeros((SizeLab[0]*SizeLab[1], 4))
        self.AccionPosible = 0
        self.EstadoSiguiente = 0
        self.alpha = 0.9
        self.gamma = 0.95
        self.Recompensa = 0
    
    def __CrearMatrizReco(self):
        TotalCas = self.SizeLab[1]*self.SizeLab[0]
        M = np.zeros((TotalCas,4))
        NumMaxCas = self.LabMat[::].max()
        for Y in range(self.SizeLab[1]):
            for X in range(self.SizeLab[0]):
                numCasilla = int((X+1) + ((Y)*(self.SizeLab[1])))
                Coor =[ [X-1,Y,0], [X,Y-1,1], [X,Y+1,2],  [X+1,Y,3] ]
                for cx,cy,cont in Coor:
                    if cx >= 0 and cy >= 0 and cx <= self.SizeLab[0]-1  and cy <= self.SizeLab[1]-1:
                        if self.LabMat[cy][cx] != 0:
                            M[numCasilla-1][cont] = 1
                            if self.LabMat[cy][cx] == self.EstadoMeta:
                                M[numCasilla-1][cont] = 10

        return M

    def __CrearMatrizLab(self):
        M = np.zeros((self.SizeLab[1], self.SizeLab[0]))
        for y in range(self.SizeLab[1]):
            for x in range(self.SizeLab[
                0]):
                numCasilla = int((x+1) + ((y)*(self.SizeLab[1])))
                if not numCasilla in self.EdoNegro:
                    M[y][x] = numCasilla
                else:
                    M[y][x] = 0
        return M

    def SeleccionarAccion(self):
        Valores=[]
        direc=[]    
        for num, Acc in enumerate(self.MatReco[self.EstadoActual-1][:]):
            if Acc!=0:
                Valores.append(self.MatReco[self.EstadoActual-1][num])
                direc.append(num)
        if len(direc)==1:
            self.AccionPosible = direc[0]
            return self.EstadoActual, self.AccionPosible
        EstadosProb=[]
        for i in range(len(direc)):
            Estado=self.BuscaEstado(direc[i],self.EstadoActual)
            Val=[]
            for Accion2 in range(len(self.MatReco[self.EstadoActual-1][:])):
                if self.MatReco[Estado-1][Accion2]!=0:
                    Val.append(self.MatrizQ[Estado-1][Accion2])
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
        self.AccionPosible=direc[Valor2]
        return self.EstadoActual, self.AccionPosible

    def BuscaEstado(self, Accion, PosicionI):
        x,y = self.ObtenerCoordenadas(PosicionI)
        if Accion == 0:
            x-=1
        elif Accion ==1:
            y-=1
        elif Accion ==2:
            y+=1
        else:
            x+=1
        return int(self.LabMat[y][x])

    def ObtenerCoordenadas(self, Posicion):
        for y in range(len(self.LabMat[:][0])):
            for x in  range(len(self.LabMat[0][:])):
                if Posicion == self.LabMat[y][x]:
                    return x, y
        raise

    def MoverRobotSigCasilla(self, EdoAnt, Accion):
        self.EstadoSiguiente = self.BuscaEstado(Accion, EdoAnt)
        return self.EstadoSiguiente

    def ObtenerRecompensa(self, Edo, Accion):
        self.Recompensa =  self.MatReco[Edo-1, Accion]
        return self.MatReco[Edo-1, Accion]

    def ActualizacionQ(self, EdoAnt, Accion, Reco, EdoSig):
        Edo=self.EstadoActual-1
        EdoSig=self.EstadoSiguiente-1
        MaximoEdoSig=self.MaxEdoSig()
        AccPos = self.AccionPosible 
        self.MatrizQ[Edo][AccPos] = self.MatrizQ[Edo][AccPos]+self.alpha*(self.Recompensa+self.gamma*MaximoEdoSig \
                                    -self.MatrizQ[Edo][AccPos])
        self.EstadoActual = self.EstadoSiguiente
        return self.MatrizQ
    
    def MaxEdoSig(self):
        vec=self.MatReco[self.EstadoSiguiente-1][:]
        Maxim=[]
        r=0
        for i in range(len(vec)):
            if vec[i]==0:
                Maxim.append(-math.inf)
            else:
                Maxim.append(self.MatrizQ[self.EstadoSiguiente-1][i])
        return(max(Maxim))
        

# if __name__ == "__main__":
#     EspNeg = [6,9,10,11,13,16,18,22,23,25,26,27,32,37,38,39,41,42]
#     Robot1 = Robot(EdoNegro = EspNeg)
#     edo1, Acc = Robot1.SeleccionarAccion()
#     edo2 = Robot1.MoverRobotSigCasilla(edo1, Acc)
#     Reco = Robot1.ObtenerRecompensa(edo1, Acc)
#     print(Robot1.ActualizacionQ(edo1, Acc, Reco, edo2))
#     pass