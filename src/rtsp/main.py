import Jetson.GPIO as GPIO
import time
import os
import subprocess

#subprocess.run('python3 web_streaming.py')


pwm_pin_motor_rechts = 32
pwm_pin_motor_links = 33

# Controller Variable hier setzen
controller = "xbox"
# controller = "ps4"
def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

if(controller == "xbox"):
    import xboxcontroller
elif(controller == "ps4"):
    import ps4controller
else:
    print("Falsche Controller Variable: ps4/xbox")

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(pwm_pin_motor_rechts, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pwm_pin_motor_links, GPIO.OUT,initial=GPIO.LOW)
pwm1 = GPIO.PWM(pwm_pin_motor_rechts, 100)
pwm2 = GPIO.PWM(pwm_pin_motor_links, 100)
valpwm1 = 0
valpwm2 = 0
pwm1.start(valpwm1)
pwm2.start(valpwm2)


try:
    while(True):
        ls = xboxcontroller.ausgabe("ls")
        ls = truncate(ls , 3)
        ls = ls.replace("(","")
        ls = ls.replace(",","")
        rt = xboxcontroller.ausgabe("rt")
        rt = truncate(rt , 3)
        rt = rt.replace("(","")
        rt = rt.replace(",","")
        rt = float(rt)
        valpwm2 = rt*100.0

        valpwm1 = valpwm2
        ls = float(ls)


        if(ls < 0.00):
            ls = ls * (-1)
            valpwm1 = valpwm1 * (1- ls)
            
        elif(ls >= 0.00):
            valpwm2 = valpwm2 * (1- ls)

        valpwm1 = format(valpwm1, '.1f')  
        valpwm2 = format(valpwm2, '.1f')        
        # print(valpwm1)
        # print(valpwm2)
        #print("___________")

        valpwm1 = float(valpwm1)
        valpwm2 = float(valpwm2)
        pwm1.ChangeDutyCycle(valpwm1)
        pwm2.ChangeDutyCycle(valpwm2)
        time.sleep(0.1)
finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()



#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)

#GPIO.setup(11, GPIO.OUT)
#GPIO.output(11, GPIO.HIGH)q