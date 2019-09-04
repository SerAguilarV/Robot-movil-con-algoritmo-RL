#Interfaz Gráfica
from tkinter import *    # Carga módulo tk (widgets estándar)
from tkinter import ttk

class Aplicacion():
    def __init__(self, size=(500,200)):
        self.display = Tk()
        self.display.geometry(str(size[0])+'x'+str(size[1]))
        self.display.configure(bg = 'beige')
        self.display.title('Aplicación') 
        t = ttk.Label(self.display, text = 'Hola mundo')
        self.display.mainloop()
    
if __name__ == '__main__':
    app = Aplicacion()