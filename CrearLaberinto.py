import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pt

class CrearLaberinto:
    def __init__(self):
        self.heigth = 10
        self.width = 10
    
    def ask_size(self):
        h = 0
        texto = 'Introduce cuantas casillas verticales tendra el laberinto: '
        while h<5 or h>10:
            try:
                h=int(input(texto))
            except:
                h = 0
            finally:
                texto = '\nEl numero elige un numero entre el 4 y 10.\nIntroduce cuantas casillas verticales tendra el laberinto: '
        w = 0        
        texto = 'Introduce cuantas casillas horizontales tendra el laberinto: '
        while w<5 or w>10:
            try:
                w=int(input(texto))
            except:
                w = 0
            finally:
                texto = '\nEl numero elige un numero entre el 4 y 10.\nIntroduce cuantas casillas horizontales tendra el laberinto: '
        return h,w
        
    def get_limits(self,h,w):
        lim_up = pt.Rectangle((0,h+1), w+2,1, fill = True, color='black')
        lim_down = pt.Rectangle((0,0), w+2,1, fill = True, color='black')
        lim_left = pt.Rectangle((0,0), 1, h+1, fill = True, color='black')
        lim_rigth = pt.Rectangle((w+1,0), 1, h+1, fill = True, color='black')
        return [lim_up, lim_down, lim_left, lim_rigth]
    
    def get_paths(self, path):
        patches = []
        for p in path:
            patches.append(pt.Rectangle((p[0],p[1]), 1,1, fill = True, color='black'))
        return patches

    def sizeFig(self):
        val_max = 6.5
        if self.heigth>self.width:
            y =val_max
            x = (self.width/self.heigth) * val_max
        else:
            x = val_max
            y = (self.heigth/self.width) * val_max
        return (x,y)
    
    def show_Labyrinth(self):
        fig= plt.figure()
        ax = fig.add_axes([0,0,1,1])
        imagen = plt.imread('laberinto.png')
        ax.imshow(imagen)
        ax.set_axis_off()
        plt.show(block=False)
        plt.pause(1.5)
        plt.close()
    
    def path_Labyrinth(self,h,w, size_fig):
        path = []
        goal = False
        startPosition = None
        start = False
        goalPosition = None
        while True:
            fig = plt.figure(figsize=size_fig)
            ax = fig.add_axes([0,0,1,1])
            major_ticks = np.arange(0, w+2,1)
            minor_ticks = np.arange(0, h+2,1)
            ax.set_xticks(major_ticks)
            ax.set_xticks(minor_ticks, minor=True)
            ax.set_yticks(major_ticks)
            ax.set_yticks(minor_ticks, minor=True)
            ax.grid(which='minor', alpha=0.2)
            ax.grid(which='major', alpha=0.5)
            ax.grid(True)
            ax.set_xlim([0,w+2])
            ax.set_ylim([0,h+2])
            patches = self.get_limits(h,w)
            for pat in patches:
                ax.add_patch(pat)
            if path:
                patches_path = self.get_paths(path)
                for pat in patches_path:
                    ax.add_patch(pat)
            if not goal and not startPosition:
                x = plt.ginput(n=-1, show_clicks = True)
                if not x:
                    goal = True
                    plt.close()
                    continue
                for y in x:
                    x1=y
                    path.append([int(x1[0]),int(x1[1])])
                plt.close()
                print("Ruta:\n", path)
            elif goal and not startPosition and not start:
                x = plt.ginput(n=1, show_clicks = True)
                x = x[0]
                startPosition = [int(x[0]),int(x[1])]
                plt.close()
                continue
            elif startPosition and not start:
                p = pt.Rectangle((startPosition[0],startPosition[1]), 1,1, fill = True, color='green')
                ax.add_patch(p)
                plt.close()
                goal = False
                start = True
            elif start and not goalPosition:
                p = pt.Rectangle((startPosition[0],startPosition[1]), 1,1, fill = True, color='green')
                ax.add_patch(p)
                x = plt.ginput(n=1, show_clicks = True)
                x = x[0]
                goalPosition = [int(x[0]),int(x[1])]
                plt.close()
                continue
            else:
                p = pt.Rectangle((startPosition[0],startPosition[1]), 1,1, fill = True, color='green')
                ax.add_patch(p)
                p = pt.Rectangle((goalPosition[0],goalPosition[1]), 1,1, fill = True, color='yellow')
                ax.add_patch(p)
                break
        print(path)
        BlackSpaces = self.getBlackSpaces(path, h, w)
        Inicio = self.LookFor(startPosition, h, w)
        Final = self.LookFor(goalPosition, h, w)
        plt.savefig('laberinto.png')
        plt.close()
        return BlackSpaces, Inicio, Final

    def LookFor(self, path, filas, columnas):
        conty = -1
        for y in range(filas,0,-1):
            conty+=1
            for x in range(1,columnas+1,1):
                if [x,y] == path:
                    numCasilla = (x) + ((conty)*(columnas))
                    print("Casilla Encontrada: " + str(numCasilla))
                    return numCasilla

    def getBlackSpaces(self, path, filas, columnas):
        BlackSpaces = []
        conty = -1
        for y in range(filas,0,-1):
            conty+=1
            for x in range(1,columnas+1,1):
                if [x,y] in path:
                    numCasilla = (x) + ((conty)*(columnas))
                    #print("Casilla Negra {}: {} , {}".format(numCasilla, x, conty))
                    BlackSpaces.append(numCasilla)
        print(BlackSpaces)
        return BlackSpaces

    def create_Labyrinth(self, size = None ):
        if size:
            self.heigth = size['heigth']
            self.width = size['width']
        h = self.heigth
        w = self.width
        size_fig = self.sizeFig()
        BlackSpaces, Inicio, Final = self.path_Labyrinth(h,w, size_fig)
        print('Se termino, el laberinto es el siguiente')
        self.show_Labyrinth()
        return BlackSpaces, Inicio, Final
        
# if __name__ == '__main__':
# def Main(h, w):
#     L = Labyrinth()
#     # h,w = L.ask_size()
#     L.create_Labyrinth(size = {'heigth':h, 'width':w})
#     return h,w

#Main()