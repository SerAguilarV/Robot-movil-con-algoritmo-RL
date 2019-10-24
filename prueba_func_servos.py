import time
import pigpio
import numpy as np
from control_servos import servo_p1_h, servo_p2_h, servo_p3_h, servo_p4_h, servo_p1_ah, servo_p2_ah, servo_p3_ah, servo_p4_ah


pi = pigpio.pi()

pi.set_mode(21, pigpio.OUTPUT)
pi.set_mode(20, pigpio.OUTPUT)
pi.set_mode(16, pigpio.OUTPUT)
pi.set_mode(12, pigpio.OUTPUT)

pi.set_PWM_dutycycle(21, 128)
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

#p = float(input('Introduzca la velocidad '));
servo_p1_ah(0.5)
servo_p2_h(0.5)
time.sleep(5)
#servo_p2_ah(0.8)
#time.sleep(3)
#servo_p2_ah(1)
#time.sleep(3)

pi.set_PWM_dutycycle(21, 0) #PWM off
pi.set_PWM_dutycycle(20, 0)
pi.set_PWM_dutycycle(16, 0)
pi.set_PWM_dutycycle(12, 0)

