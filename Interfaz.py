import tkinter as tk 
from PIL import Image, ImageTk
from CrearLaberinto import CrearLaberinto

Laberinto = None
RL = None
Eps = None
EspaciosNegros = []
Tamaño = []
Inicio = None
Final = None
EnableRobot = None

class WindowMain():
    def __init__(self):
        self.root = tk.Tk() 
        self.root.geometry("500x250")
        self.root.title("UPIITA")
        frame2 = tk.Frame(self.root, height=20)
        frame2.pack()

        titulo = tk.Label(self.root , text = "Trabajo Terminal 2\nRobot Movil con Q-Learning ", font = ("Helvética", "24", "bold")  ).pack(side = tk.TOP)
        frame = tk.Frame(self.root)
        frame.pack()
        Boton_1 = tk.Button(frame, text="Crear\nLaberinto", font=("Helvética", "16") , width = 15,
                command = self.functionCrearLab)
        Boton_1.pack(side = tk.LEFT, padx = 20, pady =20, )
        Boton_2 = tk.Button(frame, text="Laberinto\nPredeterminado", font=("Helvética", "16") , width = 15, 
                                command = self.functionLabDefault)
        Boton_2.pack(side = tk.RIGHT, padx = 20, pady =20)
        self.root.mainloop() 
    
    def functionLabDefault(self):
        self.root.destroy()
        W = WindowLabDefault()
    
    def functionCrearLab(self):
        self.root.destroy()
        W = WindowCrearLab()

    def GetDatosPred(self):
        global Laberinto, EspaciosNegros, RL, Eps, EnableRobot
        if EnableRobot:
            print("Abriendo Camara ...")
        return Laberinto, EspaciosNegros, RL, Eps, EnableRobot
    
    def GetDatos(self):
        global Laberinto, EspaciosNegros, RL, Eps, Tamaño, Inicio, Final, EnableRobot
        if EnableRobot:
            print("Abriendo Camara ...")
        return Laberinto, EspaciosNegros, RL, Eps, Tamaño, Inicio, Final, EnableRobot
    
    def KindLab(self):
        global Laberinto
        if Laberinto == "Creado":
            return True
        return False
        
class WindowLabDefault():
    def __init__(self):
        self.root = tk.Tk() 
        self.root.geometry("500x300")
        self.root.title("UPIITA")
        frame2 = tk.Frame(self.root, height=20)
        frame2.pack()

        titulo = tk.Label(self.root , text = "Laberintos predeterminados", font = ("Helvética", "14", "bold")  ).pack(side = tk.TOP, pady =10)
        frame = tk.Frame(self.root) 
        frame.pack()
        Boton_1 = tk.Label(frame, text="Laberinto 1", font=("Helvética", "12") , width = 15)
        Boton_1.pack(side = tk.LEFT, padx = 5, pady =10)
        Boton_2 = tk.Label(frame, text="Laberinto 2", font=("Helvética", "12") , width = 15)
        Boton_2.pack(side = tk.LEFT, padx = 5, pady =10)
        Boton_3 = tk.Label(frame, text="Laberinto 3", font=("Helvética", "12") , width = 15)
        Boton_3.pack(side = tk.LEFT, padx = 5, pady =10)

        frame3 = tk.Frame(self.root) 
        frame3.pack()
        im1 = self.__imgLab('laberinto1.png')
        img1 = tk.Button(frame3, image = im1, command = lambda : self.__Lab1Selected(1))
        img1.pack(side = tk.LEFT, padx = 5, pady =5)
        im2 = self.__imgLab('laberinto2.png')
        img2 = tk.Button(frame3, image = im2, command = lambda : self.__Lab1Selected(2))
        img2.pack(side = tk.LEFT, padx = 5, pady =5)
        im3 = self.__imgLab('Laberinto3.png')
        img3 = tk.Button(frame3, image = im3, command = lambda : self.__Lab1Selected(3))
        img3.pack(side = tk.LEFT, padx = 5, pady =5)
        self.root.mainloop() 

    def __Lab1Selected(self, data):
        self.root.destroy()
        global Laberinto
        Laberinto  = data
        WFL = WindowFeaturesLab()

    def __imgLab(self, path):
        size = 135
        img = Image.open(path)
        img = img.resize((size, size), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

class WindowFeaturesLab():
    def __init__(self):
        global Laberinto
        self.root = tk.Tk() 
        self.root.geometry("500x350")
        self.root.title("UPIITA")
        RL2 = tk.IntVar()
        EnRobot = tk.BooleanVar() 
        #RL2.set(0)
        frame2 = tk.Frame(self.root, height=20)
        frame2.pack()
        if not Laberinto:
            Laberinto = "Creado"
        titulo = tk.Label(self.root , text = "Caracteristicas para\nLaberinto {} ".format(Laberinto), font = ("Helvética", "14", "bold")  ).pack(side = tk.TOP, pady =5)
        frame = tk.Frame(self.root) 
        frame.pack()
        LabelEpisodios = tk.Label(frame , text = "Número de Episodios ".format(Laberinto), font = ("Helvética", "11")  ).pack(side = tk.LEFT)
        scale_widget = tk.Scale(frame, from_=0, to=100,orient=tk.HORIZONTAL, width=20, length =200 ,)
        scale_widget.set(25)
        scale_widget.pack(side = tk.RIGHT)

        frame3 = tk.Frame(self.root, height=20)
        frame3.pack()
        labelframe_widget = tk.LabelFrame(frame3, text="Algoritmo de Reinforcement Learning")
        radiobutton_widget1 = tk.Radiobutton(labelframe_widget, text="Q - Learning", variable=RL2, value=1)
        radiobutton_widget2 = tk.Radiobutton(labelframe_widget, text="SARSA", variable=RL2, value=2)
        radiobutton_widget3 = tk.Radiobutton(labelframe_widget, text="Backward Q - Learning", variable=RL2, value=3)
        labelframe_widget.pack(padx=20, pady=20)
        radiobutton_widget1.pack(side = tk.LEFT, padx=10)
        radiobutton_widget2.pack(side = tk.LEFT, padx=10)
        radiobutton_widget3.pack(side = tk.LEFT, padx=10)
        radiobutton_widget3.select()

        frame3 = tk.Frame(self.root, height=20)
        frame3.pack()
        labelframe_widget2 = tk.LabelFrame(frame3, text="Robot Omnidireccional")
        radiobutton_widget4 = tk.Radiobutton(labelframe_widget2, text="Con Robot", variable=EnRobot, value=True)
        radiobutton_widget5 = tk.Radiobutton(labelframe_widget2, text="Sin Robot", variable=EnRobot, value=False)
        labelframe_widget2.pack(padx=20)
        radiobutton_widget4.pack(side = tk.LEFT, padx=10)
        radiobutton_widget5.pack(side = tk.LEFT, padx=10)
        radiobutton_widget5.select()

        frame5 = tk.Frame(self.root)
        frame5.pack()
        boton1 = tk.Button(frame5, text = "Continuar", command = lambda : self.__ContinueProgram(RL2,
                                                                    scale_widget.get(), EnRobot.get()))
        boton1.pack(side = tk.TOP, pady = 30)
        self.root.mainloop() 

    def __ContinueProgram(self,v1,v2, v3):
        global EspaciosNegros, Laberinto, RL, Eps, EnableRobot
        RL = v1.get()
        Eps = v2
        EnableRobot = v3
        if Laberinto == 1:
            EspaciosNegros = [6,9,10,11,13,16,18,22,23,25,26,27,32,37,38,39,41,42]
        elif Laberinto == 2:
            EspaciosNegros = [2,3,4,5,6,9,10,11,12,13,16,17,18,19,20]
        elif Laberinto == 3:
            EspaciosNegros = []
        self.root.destroy()

class WindowCrearLab():
    def __init__(self):
        self.root = tk.Tk() 
        self.root.geometry("500x300")
        self.root.title("Crear Laberinto")
        frame2 = tk.Frame(self.root, height=20)
        frame2.pack()

        titulo = tk.Label(self.root , text = "Tamaño de Laberinto", font = ("Helvética", "14", "bold")  ).pack(side = tk.TOP, pady =5)
        frame3 = tk.Frame(self.root) 
        frame3.pack(pady =5)
        
        scale_widget = tk.Scale(frame3, from_=3, to=10,orient=tk.HORIZONTAL, width=15, length =200 , 
                        label = "Altura de Laberinto", font = ("Helvética", "10"))
        scale_widget.set(5)
        scale_widget.pack(side = tk.TOP, pady = 10)

        scale_widget2 = tk.Scale(frame3, from_=3, to=10,orient=tk.HORIZONTAL, width=15, length =200 ,
                        label = "Ancho de Laberinto" , font = ("Helvética", "10") )
        scale_widget2.set(5)
        scale_widget2.pack(side = tk.TOP, pady =10)

        frame5 = tk.Frame(self.root)
        frame5.pack(pady = 20)
        boton1 = tk.Button(frame5, text = "Continuar", command = lambda : self.__ContinueProgram(
                                                            scale_widget.get(), scale_widget2.get()))
        boton1.pack(side = tk.TOP)

        self.root.mainloop() 
        
    def __ContinueProgram(self,v1,v2):
        global EspaciosNegros, Tamaño, Inicio, Final
        #print("Altura de Laberinto: {}".format(v1))
        #print("Ancho de Laberinto: {}".format(v2))
        Tamaño = [v1,v2]
        self.root.destroy()
        L = CrearLaberinto()
        EspaciosNegros, Inicio, Final = L.create_Labyrinth(size = {'heigth':v1, 'width':v2})
        WFL = WindowFeaturesLab()


# if __name__ is "__main__":
#     W = WindowFeaturesLab()
    # W = WindowMain()
    # L, EN, R, E  = W.GetDatos()
    # print("Laberinto: {}".format(L))
    # print("Espacios en Negro: {}".format(EN))
    # print("RL: {}".format(R))
    # print("Episodios: {}".format(E))
