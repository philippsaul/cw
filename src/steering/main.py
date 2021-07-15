import Jetson.GPIO as GPIO
import time
import os
import subprocess
from ps4 import Controller
import threading


pwm_pin_motor_rechts = 32
pwm_pin_motor_links = 33
pin_motor_rechts_vor = 35
pin_motor_rechts_zurueck = 36
pin_motor_links_vor = 37
pin_motor_links_zurueck = 38


#Folgender Wert kann pro Controller angepasst werden
con_thr = 0.05                      #definiert nicht berüksichtigte Eingaben vom Gamepad / von 0 bis +/-con_thr

anlaufboost = True                  #setzt Anfangszustand, um den Anlaufwiderstand der Motoren zu überwinden; nicht verändern

#Folgenden vier Werte können pro JetBot angepasst werden
aim_boost = 35.00                   #definiert den kurzeitigen Zielzustand, um den Anlaufwiderstand zu überwinden
min_load = 25.00                    #definiert das geringst möglich PWM Signal von 0 bis 100, sodass die Motoren nach Überwindung des Anlaufwiderstandes noch funktionieren
circle_thr_max = 35.00              #"Radius" bezogen auf PWM Kurve
circle_thr_min = 25.00

tempomat = False                   #definiert Start-Zustand für Tempomat; nicht verändern


tem_val = 0
tem_vel = 0.0


# Controller Variable hier setzen
# controller = "xbox"
controller = "ps4"


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
    ps4 = Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)
    ps4_thread = threading.Thread(target=ps4.listen, name="test")
    ps4_thread.start()
    while ps4.ls != 0 and ps4.lt != 0 and ps4.rt != 0:
        continue
else:
    print("Falsche Controller Variable: ps4/xbox")

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
valpwm1 = 0
valpwm2 = 0
pwm1.start(valpwm1)
pwm2.start(valpwm2)


try:
    while(True):
        if(controller == "xbox"):
            ls = xboxcontroller.ausgabe("ls")
            ls = truncate(ls , 3)
            ls = ls.replace("(","")
            ls = ls.replace(",","")
            rt = xboxcontroller.ausgabe("rt")
            rt = truncate(rt , 3)
            rt = rt.replace("(","")
            rt = rt.replace(",","")
            rt = float(rt)
            ls = float(ls)
            lt = xboxcontroller.ausgabe("lt")
            lt = truncate(lt , 3)
            lt = lt.replace("(","")
            lt = lt.replace(",","")
            lt = float(lt)

            #Buttonabfrage für Tempomat
            yb = xboxcontroller.ausgabe("yb")
            ab = xboxcontroller.ausgabe("ab")
            bb = xboxcontroller.ausgabe("bb")
            xb = xboxcontroller.ausgabe("xb")

        elif(controller == "ps4"):
            # ls = (ps4.ls + 32767)/65534
            ls = ps4.ls/32767
            rt = (ps4.rt + 32767)/65534
            lt = (ps4.lt + 32767)/65534
            yb = ps4.yb
            ab = ps4.ab
            bb = ps4.bb
            xb = ps4.xb

        else:
            print("Falsche Controller Variable: ps4/xbox")

        
        if(bb == 1):
            tempomat = False
            tem_val = 0
        elif(xb == 1):
            tempomat = True

        # print(tempomat)
        # print(lt)
        # print(rt)
        # print(ls)
        # print(xb)


        if(tempomat):
            if(yb == 1) and (tem_val < 3):
                tem_val = tem_val + 1
            elif(ab == 1) and (tem_val > 0):
                tem_val = tem_val - 1


            if(tem_val == 0):
                
                if (ls >= con_thr):
                    GPIO.output(pin_motor_rechts_vor, GPIO.LOW)
                    GPIO.output(pin_motor_rechts_zurueck, GPIO.HIGH)
                    GPIO.output(pin_motor_links_zurueck, GPIO.LOW)
                    GPIO.output(pin_motor_links_vor, GPIO.HIGH)

                    # valpwm1 = ls*100.00
                    # valpwm2 = valpwm1
                    valpwm1 = 30
                    valpwm2 = 30

                    anlaufboost = False

                elif (ls <= (-con_thr)):
                    GPIO.output(pin_motor_rechts_zurueck, GPIO.LOW)
                    GPIO.output(pin_motor_rechts_vor, GPIO.HIGH)
                    GPIO.output(pin_motor_links_vor, GPIO.LOW)
                    GPIO.output(pin_motor_links_zurueck, GPIO.HIGH)

                    # valpwm1 = -(ls*100.00)
                    # valpwm2 = valpwm1
                    valpwm1 = 30
                    valpwm2 = 30

                    anlaufboost = False

                elif ((ls <= con_thr) or (ls>= (-con_thr))):
                    GPIO.output(pin_motor_rechts_vor, GPIO.HIGH)    
                    GPIO.output(pin_motor_rechts_zurueck, GPIO.HIGH)
                    GPIO.output(pin_motor_links_vor, GPIO.HIGH)
                    GPIO.output(pin_motor_links_zurueck, GPIO.HIGH)

                    valpwm1 = 100.00
                    valpwm2 = 100.00

                    anlaufboost = True

            else:
                if(tem_val == 1):
                    tem_vel = 0.0
                elif(tem_val == 2):
                    tem_vel = 0.5
                elif(tem_val == 3):
                    tem_vel = 1
                
                # print(tem_vel)
                GPIO.output(pin_motor_rechts_zurueck, GPIO.LOW)
                GPIO.output(pin_motor_rechts_vor, GPIO.HIGH)
                GPIO.output(pin_motor_links_zurueck, GPIO.LOW)
                GPIO.output(pin_motor_links_vor, GPIO.HIGH)

                if(rt > tem_vel):
                    tem_vel = rt

                valpwm2 = tem_vel * (100.0 - min_load) + min_load
                valpwm1 = valpwm2
                circle_act = circle_thr_min + (circle_thr_max - circle_thr_min) * tem_vel

                if(ls < 0.00):
                    ls = ls * (-1)
                    valpwm2 = valpwm2 + circle_act * ls
                    valpwm1 = valpwm1 - circle_act * ls

                elif(ls >= 0.00):
                    valpwm1 = valpwm1 + circle_act * ls
                    valpwm2 = valpwm2 - circle_act * ls

                if(valpwm1 > 100.00):
                    valpwm2 = valpwm2 - (valpwm1 - 100.00)
                    valpwm1 = 100.0
                elif(valpwm1 < min_load):
                    valpwm2 = valpwm2 + (min_load - valpwm1)
                    valpwm1 = min_load
                elif(valpwm2 > 100.00):
                    valpwm1 = valpwm1 - (valpwm2 - 100.00)
                    valpwm2 = 100.0
                elif(valpwm2 < min_load):
                    valpwm1 = valpwm1 + (min_load - valpwm2)
                    valpwm2 = min_load

                if(anlaufboost):
                    anlaufboost = False
                    valpwm1 = aim_boost
                    valpwm2 = aim_boost

        
        elif(rt > 0.00) and (lt <= con_thr):                        #setze PWM bei Fahrt nach vorne
            GPIO.output(pin_motor_rechts_zurueck, GPIO.LOW)
            GPIO.output(pin_motor_rechts_vor, GPIO.HIGH)
            GPIO.output(pin_motor_links_zurueck, GPIO.LOW)
            GPIO.output(pin_motor_links_vor, GPIO.HIGH)

            valpwm2 = rt * (100.0 - min_load) + min_load
            valpwm1 = valpwm2
            circle_act = circle_thr_min + (circle_thr_max - circle_thr_min) * rt
            
            if(ls < 0.00):
                ls = ls * (-1)
                valpwm2 = valpwm2 + circle_act * ls
                valpwm1 = valpwm1 - circle_act * ls

            elif(ls >= 0.00):
                valpwm1 = valpwm1 + circle_act * ls
                valpwm2 = valpwm2 - circle_act * ls

            if(valpwm1 > 100.00):
                valpwm2 = valpwm2 - (valpwm1 - 100.00)
                valpwm1 = 100.0
            elif(valpwm1 < min_load):
                valpwm2 = valpwm2 + (min_load - valpwm1)
                valpwm1 = min_load
            elif(valpwm2 > 100.00):
                valpwm1 = valpwm1 - (valpwm2 - 100.00)
                valpwm2 = 100.0
            elif(valpwm2 < min_load):
                valpwm1 = valpwm1 + (min_load - valpwm2)
                valpwm2 = min_load

            if(anlaufboost):
                anlaufboost = False
                valpwm1 = aim_boost
                valpwm2 = aim_boost
        
        elif(lt > 0.00) and (rt <= con_thr) and (not tempomat):
            GPIO.output(pin_motor_rechts_vor, GPIO.LOW)
            GPIO.output(pin_motor_rechts_zurueck, GPIO.HIGH)
            GPIO.output(pin_motor_links_vor, GPIO.LOW)
            GPIO.output(pin_motor_links_zurueck, GPIO.HIGH)

            valpwm2 = lt * (100.0 - min_load) + min_load
            valpwm1 = valpwm2
            circle_act = circle_thr_min + (circle_thr_max - circle_thr_min) * lt
            
            if(ls < 0.00):
                ls = ls * (-1)
                valpwm2 = valpwm2 + circle_act * ls
                valpwm1 = valpwm1 - circle_act * ls

            elif(ls >= 0.00):
                valpwm1 = valpwm1 + circle_act * ls
                valpwm2 = valpwm2 - circle_act * ls

            if(valpwm1 > 100.00):
                valpwm2 = valpwm2 - (valpwm1 - 100.00)
                valpwm1 = 100.0
            elif(valpwm1 < min_load):
                valpwm2 = valpwm2 + (min_load - valpwm1)
                valpwm1 = min_load
            elif(valpwm2 > 100.00):
                valpwm1 = valpwm1 - (valpwm2 - 100.00)
                valpwm2 = 100.0
            elif(valpwm2 < min_load):
                valpwm1 = valpwm1 + (min_load - valpwm2)
                valpwm2 = min_load

            if(anlaufboost):
                anlaufboost = False
                valpwm1 = aim_boost
                valpwm2 = aim_boost

        elif (rt == 0.0) and (lt == 0.0) and (ls >= con_thr):
            GPIO.output(pin_motor_rechts_vor, GPIO.LOW)
            GPIO.output(pin_motor_rechts_zurueck, GPIO.HIGH)
            GPIO.output(pin_motor_links_zurueck, GPIO.LOW)
            GPIO.output(pin_motor_links_vor, GPIO.HIGH)

            # valpwm1 = ls*100.00
            # valpwm2 = valpwm1
            valpwm1 = 30
            valpwm2 = 30

            anlaufboost = False

        elif (rt == 0.0) and (lt == 0.0) and (ls <= (-con_thr)):
            GPIO.output(pin_motor_rechts_zurueck, GPIO.LOW)
            GPIO.output(pin_motor_rechts_vor, GPIO.HIGH)
            GPIO.output(pin_motor_links_vor, GPIO.LOW)
            GPIO.output(pin_motor_links_zurueck, GPIO.HIGH)

            # valpwm1 = -(ls*100.00)
            # valpwm2 = valpwm1
            valpwm1 = 30
            valpwm2 = 30

            anlaufboost = False

        elif (rt <=con_thr) and (lt <=con_thr) and ((ls <= con_thr) or (ls>= (-con_thr)) and (not tempomat)):
            GPIO.output(pin_motor_rechts_vor, GPIO.HIGH)    
            GPIO.output(pin_motor_rechts_zurueck, GPIO.HIGH)
            GPIO.output(pin_motor_links_vor, GPIO.HIGH)
            GPIO.output(pin_motor_links_zurueck, GPIO.HIGH)

            valpwm1 = 100.00
            valpwm2 = 100.00

            anlaufboost = True
        
        
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