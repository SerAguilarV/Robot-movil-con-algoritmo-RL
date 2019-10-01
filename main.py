import tkinter as tk 

class window():
    def __init__(self):
        root = tk.Tk() 
        root.geometry("500x250")
        root.title("UPIITA")
        frame2 = tk.Frame(root, height=20)
        frame2.pack()

        titulo = tk.Label(root , text = "Trabajo Terminal 2\nRobot Movil con Q-Learning ", font = ("Helvética", "24", "bold")  ).pack(side = tk.TOP)
        frame = tk.Frame(root)
        frame.pack()
        Boton_1 = tk.Button(frame, text="Crear\nLaberinto", font=("Helvética", "16") , width = 15)
        Boton_1.pack(side = tk.LEFT, padx = 20, pady =20)
        Boton_2 = tk.Button(frame, text="Laberinto\nPredeterminado", font=("Helvética", "16") , width = 15)
        Boton_2.pack(side = tk.RIGHT, padx = 20, pady =20)
        root.mainloop() 

if __name__ is "__main__":
    w = window()

