import Jetson.GPIO as GPIO
import time
import threading
import settings

# später über Controller Lib
# from controller.ps4 import controller    


#definition of motor control pins on Jetson Nano
pwm_pin_motor_rechts = 32
pwm_pin_motor_links = 33
pin_motor_rechts_vor = 35
pin_motor_rechts_zurueck = 36
pin_motor_links_vor = 37
pin_motor_links_zurueck = 38

#set working variable for working control
anlaufboost = True
tempomat = False
tem_val = 0
tem_vel = 0.0
valpwm1 = 0
valpwm2 = 0

#initialize motor controll + customized data once
def initialize():
    liste = settings.userdata()
    con_thr = liste[1]
    aim_boost = liste[2]                  
    min_load = liste[3]                    
    circle_thr_max = liste[4]            
    circle_thr_min = liste[5]

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    GPIO.setup(pwm_pin_motor_rechts, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pwm_pin_motor_links, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(pin_motor_rechts_vor, GPIO.OUT, initial=GPIO.LOW)       #setup direction status
    GPIO.setup(pin_motor_rechts_zurueck, GPIO.OUT, initial=GPIO.LOW)       #setup direction status
    GPIO.setup(pin_motor_links_vor, GPIO.OUT, initial=GPIO.LOW)       #setup direction status
    GPIO.setup(pin_motor_links_zurueck, GPIO.OUT, initial=GPIO.LOW)       #setup direction status
    pwm1 = GPIO.PWM(pwm_pin_motor_rechts, 100)
    pwm2 = GPIO.PWM(pwm_pin_motor_links, 100)
    pwm1.start(valpwm1)
    pwm2.start(valpwm2)
    

#formate pwm 
def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])