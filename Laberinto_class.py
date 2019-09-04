import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.patches as pt


class Laberinto:
    def __init__(self):
        self.heigth = 10
        self.width = 10
        
    def crear_Laberinto2(self, size = None ):
        fig = plt.figure()
        if size:
            self.heigth = size['heigth']
            self.width = size['width']
        h = self.heigth
        w = self.width
        ax = fig.add_axes([0,0,1,1])
        major_ticks = np.arange(0, h+2,1)
        minor_ticks = np.arange(0, w+2,1)
        ax.set_xticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)
        ax.set_yticks(major_ticks)
        ax.set_yticks(minor_ticks, minor=True)
        #ax.grid(color='b',which='both',  linestyle='-', linewidth=2, alpha = 0.5)
        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)
        ax.grid(True)
        ax.set_xlim([0,h+2])
        ax.set_ylim([0,w+2])
        for i in range(w+2):
            p = pt.Rectangle((0,i), 1,1, fill = True, color='red')
            p2 = pt.Rectangle((h+1,i), 1,1, fill = True, color='red')
            ax.add_patch(p)
            ax.add_patch(p2)
        for i in range(h+2):
            p = pt.Rectangle((i,0), 1,1, fill = True, color='red')
            p2 = pt.Rectangle((i,w+1), 1,1, fill = True, color='red')
            ax.add_patch(p)
            ax.add_patch(p2)
        x = plt.ginput(n=-1, show_clicks = True)
        ruta = []
        for i in x:
            a = i[0]
            b = i[1]    
            ruta.append([a,b])
        print("Ruta:\n", ruta)
        plt.close()
        plt.show()
        
    def crear_Laberinto(self, size = None ):
        if size:
            self.heigth = size['heigth']
            self.width = size['width']
        plt.xlim([0, self.heigth+2])
        plt.ylim([0, self.width+2])

        
        plt.grid(True)
        print("Ingresa los puntos de la figura que deseas que aprenda el robot."
              + "\n(Para terminar )")
        x = plt.ginput(n=-1, show_clicks = True)
        ruta = []
        for i in x:
            a = i[0]
            b = i[1]    
            ruta.append([a,b])
        print("Ruta:\n", ruta)
        plt.close()
        plt.show()
        
        
if __name__ == '__main__':
    L = Laberinto()
    L.crear_Laberinto2(size = {'heigth':10, 'width':6})