#@author: JoseMaria

import time
import pigpio
import numpy as np

pi = pigpio.pi()

#GPIO.setmode(GPIO.BCM)   #Ponemos la Raspberry en modo BOARD
#GPIO.setwarnings(False)

#pi.start()
pi.set_mode(21, pigpio.OUTPUT)
pi.set_mode(20, pigpio.OUTPUT)
pi.set_mode(16, pigpio.OUTPUT)
pi.set_mode(12, pigpio.OUTPUT)


pi.set_PWM_dutycycle(21, 128) #PWM off
pi.set_PWM_dutycycle(20, 128)
pi.set_PWM_dutycycle(16, 128)
pi.set_PWM_dutycycle(12, 128)

pi.set_PWM_frequency(21, 50)
pi.set_PWM_frequency(20, 50)
pi.set_PWM_frequency(16, 50)
pi.set_PWM_frequency(12, 50)

pi.set_servo_pulsewidth(21,1450)
pi.set_servo_pulsewidth(20,1475)
pi.set_servo_pulsewidth(16,1400)
pi.set_servo_pulsewidth(12,1450)

v = np.array([0,0.2,0.4,0.6,0.8,1])

for p in v:
    vel = 1450 - p*450
    pi.set_servo_pulsewidth(21,vel)
    time.sleep(3)

pi.set_PWM_dutycycle(21, 0) #PWM off
pi.set_PWM_dutycycle(20, 0)
pi.set_PWM_dutycycle(16, 0)
pi.set_PWM_dutycycle(12, 0)
#Detenemos el servo 
#GPIO.cleanup()



"""
try:
                
    while True:      #iniciamos un loop infinito
        p = int(input('Introduzca sentido de giro P3: '));
        

        #ang0 = 2400 - round((a0*10)/1.125,1);
        #ang1 = 2300 - round((a1*10)/1,1);
        #ang2 = 2500 - round((a2*10)/1.125,1);

 
        #pi.set_servo_pulsewidth(21,p)
        pi.set_servo_pulsewidth(20,p)
        #pi.set_servo_pulsewidth(16,p)
        #pi.set_servo_pulsewidth(12,p)
        
        #time.sleep(1)           #pausa de medio segundo

except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...

        pi.set_PWM_dutycycle(21, 0) #PWM off
        pi.set_PWM_dutycycle(20, 0)
        pi.set_PWM_dutycycle(16, 0)
        pi.set_PWM_dutycycle(12, 0)
        #Detenemos el servo 
        #GPIO.cleanup()                #Limpiamos los pines GPIO de la Raspberry y cerramos el script
"""
