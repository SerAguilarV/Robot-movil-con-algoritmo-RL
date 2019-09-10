import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pt

class Labyrinth:
    def __init__(self):
        self.heigth = 10
        self.width = 10
    
    def ask_size(self):
        h = 0
        texto = 'Introduce cuantas casillas verticales tendra el laberinto: '
        while h<6 or h>10:
            try:
                h=int(input(texto))
            except:
                h = 0
            finally:
                texto = '\nEl numero elige un numero entre el 4 y 10.\nIntroduce cuantas casillas verticales tendra el laberinto: '
        w = 0        
        texto = 'Introduce cuantas casillas horizontales tendra el laberinto: '
        while w<6 or w>10:
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
        goal_position = None
        start = False
        start_position = None
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
            if not goal and not goal_position:
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
            elif goal and not goal_position and not start:
                x = plt.ginput(n=1, show_clicks = True)
                x = x[0]
                goal_position = [int(x[0]),int(x[1])]
                plt.close()
                continue
            elif goal_position and not start:
                p = pt.Rectangle((goal_position[0],goal_position[1]), 1,1, fill = True, color='green')
                ax.add_patch(p)
                plt.close()
                goal = False
                start = True
            elif start and not start_position:
                p = pt.Rectangle((goal_position[0],goal_position[1]), 1,1, fill = True, color='green')
                ax.add_patch(p)
                x = plt.ginput(n=1, show_clicks = True)
                x = x[0]
                start_position = [int(x[0]),int(x[1])]
                plt.close()
                continue
            else:
                p = pt.Rectangle((goal_position[0],goal_position[1]), 1,1, fill = True, color='green')
                ax.add_patch(p)
                p = pt.Rectangle((start_position[0],start_position[1]), 1,1, fill = True, color='blue')
                ax.add_patch(p)
                break
        plt.savefig('laberinto.png')
        plt.close()

    
    def create_Labyrinth(self, size = None ):
        if size:
            self.heigth = size['heigth']
            self.width = size['width']
        h = self.heigth
        w = self.width
        size_fig = self.sizeFig()
        self.path_Labyrinth(h,w, size_fig)
        print('Se termino, el laberinto es el siguiente')
        self.show_Labyrinth()
        
if __name__ == '__main__':
    L = Labyrinth()
    h,w = L.ask_size()
    L.create_Labyrinth(size = {'heigth':h, 'width':w})
