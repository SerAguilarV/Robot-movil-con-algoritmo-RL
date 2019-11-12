import Interfaz
from Prueba_Lab_Ant import Iniciar

if __name__ == "__main__":
    WinMain = Interfaz.WindowMain()
    if not WinMain.KindLab():
        Laberinto, EspaciosNegros, RL, Eps, EnableRobot = WinMain.GetDatosPred()
        Iniciar(Eps, Laberinto, RL, EspaciosNegros, RobotEnable=EnableRobot )
    else:
        Laberinto, EspaciosNegros, RL, Eps, Tamaño, Inicio, Final, EnableRobot = WinMain.GetDatos()
        print("{}, {}, {}, {}, {}, {}, {}".format(Laberinto, EspaciosNegros, RL, Eps, Tamaño, Inicio, Final))
        Iniciar(NumeroEpisodios = Eps, Laberinto = Laberinto, RL = RL, EspaciosNegros = EspaciosNegros, 
                                sizeLab = Tamaño, Inicio = Inicio, Fin  = Final, RobotEnable=EnableRobot)