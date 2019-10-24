import time
import pigpio


class RobotOmnidireccional():
    def __init__(self, Llantas = [21,20,16,12], PulseWidth = [1450, 1475, 1400, 1450],
                ):
        self.pi = pigpio.pi()
        self.Llantas = Llantas
        self.PulseWidth = PulseWidth
        self.VecVel = [350, 350, 325, 500]
        for Llanta, i  in enumerate(Llantas):
            self.pi.set_mode(Llanta, pigpio.OUTPUT)
            self.pi.set_PWM_dutycycle(Llanta, 128)
            self.pi.set_PWM_frequency(Llanta, 50)
            self.pi.set_servo_pulsewidth(Llanta,PulseWidth[i])
        self.Stop()     
    
    def Run(self, Llanta, SentidoHorario, Vel):
        if Vel>1:
            Vel = 1
        if SentidoHorario:
            Rev= self.PulseWidth[Llanta-1] + Vel*self.VecVel[Llanta]
            self.pi.set_servo_pulsewidth(self.Llantas[Llanta],Rev)
            return Rev
        else:
            Rev= self.PulseWidth[Llanta-1] - Vel*self.Vel[Llanta]
            self.pi.set_servo_pulsewidth(self.Llantas[Llanta],Rev)
            return Rev
    
    def Stop(self):
        for Llanta in self.Llantas:
            self.pi.set_PWM_dutycycle(Llanta, 0) #PWM off

if __name__ == "__main__":
    RobotOmni = RobotOmnidireccional()
    while True:
        try:
            Inst = input("Ingresa Instruccion: ")
            Llanta = Inst[0]
            Sentido = Inst[1]
            Vel = int(Inst[2]) / 10
            RobotOmni.Run(Llanta,Sentido,Vel)
        except:
            RobotOmni.Stop()
