import Interfaz
from Prueba_Lab_Ant import Iniciar

if __name__ == "__main__":
    WinMain = Interfaz.WindowMain()
    if not WinMain.KindLab():
        Laberinto, EspaciosNegros, RL, Eps  = WinMain.GetDatosPred()
        Iniciar(Laberinto, EspaciosNegros, RL, Eps)
    else:
        Laberinto, EspaciosNegros, RL, Eps, Tamaño, Inicio, Final = WinMain.GetDatos()
        print("{}, {}, {}, {}, {}, {}, {}".format(Laberinto, EspaciosNegros, RL, Eps, Tamaño, Inicio, Final))
        
        #Iniciar(E, L, R, EN, Size = [], Inicio = [], Fin = 0)
    # L, EN, R, EN  = WinMain.GetDatos()
    # L = 1
    # EN = [6,9,10,11,13,16,18,22,23,25,26,27,32,37,38,39,41,42]
    # R  = 1
    # E = 30
    # print("Laberinto: {}".format(L))
    # print("Espacios en Negro: {}".format(EN))
    # print("RL: {}".format(R))
    # print("Episodios: {}".format(E))
    # LabImg = Laberinto_Img()
    # LabImg.CapturarLaberinto()
    # LabImg.MostrarLaberinto()
    # LabImg.RecortarLaberinto()
    # x = LabImg.sizeLab