import tkinter as tk 
from PIL import Image, ImageTk

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
        Boton_1 = tk.Button(frame, text="Crear\nLaberinto", font=("Helvética", "16") , width = 15)
        Boton_1.pack(side = tk.LEFT, padx = 20, pady =20)
        Boton_2 = tk.Button(frame, text="Laberinto\nPredeterminado", font=("Helvética", "16") , width = 15)
        Boton_2.pack(side = tk.RIGHT, padx = 20, pady =20)
        self.root.mainloop() 
    
    def functionLabDefault(self):
        self.root.destroy()
        

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
        img1 = tk.Button(frame3, image = im1 )
        img1.pack(side = tk.LEFT, padx = 5, pady =5)
        im2 = self.__imgLab('laberinto2.png')
        img2 = tk.Button(frame3, image = im2 )
        img2.pack(side = tk.LEFT, padx = 5, pady =5)
        im3 = self.__imgLab('Laberinto3.png')
        img3 = tk.Button(frame3, image = im3 )
        img3.pack(side = tk.LEFT, padx = 5, pady =5)
        self.root.mainloop() 

    def __imgLab(self, path):
        size = 135
        img = Image.open(path)
        img = img.resize((size, size), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

if __name__ is "__main__":
    W = WindowLabDefault()

