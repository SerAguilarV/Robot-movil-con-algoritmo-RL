import Interfaz
from Prueba_Lab_Ant import Iniciar

if __name__ == "__main__":
    WinMain = Interfaz.WindowMain()
    if not WinMain.KindLab():
        Laberinto, EspaciosNegros, RL, Eps, EnableRobot = WinMain.GetDatosPred()
        if RL != 4:
            Iniciar(Eps, Laberinto, RL, EspaciosNegros, RobotEnable=EnableRobot )
        else:
            for i in range(3):
                Iniciar(Eps, Laberinto, i+1, EspaciosNegros, RobotEnable=EnableRobot )
    else:
        Laberinto, EspaciosNegros, RL, Eps, Tamaño, Inicio, Final, EnableRobot = WinMain.GetDatos()
        # print("{}, {}, {}, {}, {}, {}, {}".format(Laberinto, EspaciosNegros, RL, Eps, Tamaño, Inicio, Final))
        if RL != 4:
            Iniciar(NumeroEpisodios = Eps, Laberinto = Laberinto, RL = RL, EspaciosNegros = EspaciosNegros, 
                                sizeLab = Tamaño, Inicio = Inicio, Fin  = Final, RobotEnable=EnableRobot)
        else:
            for i in range(3):
                Iniciar(NumeroEpisodios = Eps, Laberinto = Laberinto, RL = i+1, EspaciosNegros = EspaciosNegros, 
                                sizeLab = Tamaño, Inicio = Inicio, Fin  = Final, RobotEnable=EnableRobot)