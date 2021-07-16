import Jetson.GPIO as GPIO
import time
import threading
import configparser
import socket


class Motors:
    def __init__(self):
        #definition of motor control pins on Jetson Nano
        self.pwm_pin_motor_rechts = 32
        self.pwm_pin_motor_links = 33
        self.pin_motor_rechts_vor = 35
        self.pin_motor_rechts_zurueck = 36
        self.pin_motor_links_vor = 37
        self.pin_motor_links_zurueck = 38

        #set working variable for working control
        self.anlaufboost = True
        self.tempomat = False
        self.tem_val = 0
        self.tem_vel = 0.0
        self.valpwm1 = 0
        self.valpwm2 = 0
        self.pwm1= 0
        self.pwm2 = 0
        self.con_thr = 0
        self.aim_boost = 0                  
        self.min_load = 0                    
        self.circle_thr_max = 0            
        self.circle_thr_min = 0


        self.config = configparser.ConfigParser()
        self.config.read('./settings.ini')
        for section in self.config.sections():
            if self.config[section]['hostname'] == socket.gethostname():
                self.section = self.config[section]
                break
        if self.section == None:
            raise Exception("can't find hostname in settings.ini")

        self.con_thr = float(self.section["deadzone_throttle"])
        self.aim_boost = float(self.section["anlauf_boost"])                  
        self.min_load = float(self.section["minimal_load"])                    
        self.circle_thr_max = float(self.section["radius"])           
        self.circle_thr_min = float(self.section["minimal_kurven_radius"])

        #setup jetson GPIOs for h-bridge
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.pwm_pin_motor_rechts, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pwm_pin_motor_links, GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.pin_motor_rechts_vor, GPIO.OUT, initial=GPIO.LOW)       #setup direction status
        GPIO.setup(self.pin_motor_rechts_zurueck, GPIO.OUT, initial=GPIO.LOW)       #setup direction status
        GPIO.setup(self.pin_motor_links_vor, GPIO.OUT, initial=GPIO.LOW)       #setup direction status
        GPIO.setup(self.pin_motor_links_zurueck, GPIO.OUT, initial=GPIO.LOW)       #setup direction status
        self.pwm1 = GPIO.PWM(self.pwm_pin_motor_rechts, 100)
        self.pwm2 = GPIO.PWM(self.pwm_pin_motor_links, 100)

        #start pwm session
        self.pwm1.start(self.valpwm1)
        self.pwm2.start(self.valpwm2)

    #clean up the GPIOs and PWM session
    def clean (self):
        self.pwm1.stop()
        self.pwm2.stop()
        GPIO.cleanup()

    def __del__ (self):
        self.clean()
    
    #Base function to set the GPIOs for h bridge direction control
    #PINs are defined that way to avoid a short and stop of motors if not wanted
    def setPins(self, vallf, vallb, valrf, valrb):
        # falls rechts vorwärts fahren wollen
        if(valrf > valrb):
            GPIO.output(self.pin_motor_rechts_zurueck, GPIO.LOW)
            GPIO.output(self.pin_motor_rechts_vor, GPIO.HIGH)
        elif(valrf < valrb):
            GPIO.output(self.pin_motor_rechts_vor, GPIO.LOW)
            GPIO.output(self.pin_motor_rechts_zurueck, GPIO.HIGH)
        elif (valrf == valrb):
            GPIO.output(self.pin_motor_rechts_vor, GPIO.HIGH)
            GPIO.output(self.pin_motor_rechts_zurueck, GPIO.HIGH)
        else:
            raise Exception('wrong vallf or vallb values')

        if(vallf > vallb):
            GPIO.output(self.pin_motor_links_zurueck, GPIO.LOW)
            GPIO.output(self.pin_motor_links_vor, GPIO.HIGH)
        elif(vallf < vallb):
            GPIO.output(self.pin_motor_links_vor, GPIO.LOW)
            GPIO.output(self.pin_motor_links_zurueck, GPIO.HIGH)
        elif (vallf == vallb):
            GPIO.output(self.pin_motor_links_vor, GPIO.HIGH)
            GPIO.output(self.pin_motor_links_zurueck, GPIO.HIGH)
        else:
            raise Exception('wrong vallf or vallb values')

    #Base function for setting PWM Pins to targeted value
    def setPWM(self, lm, rm):
        lm = format(lm, '.1f')  
        rm = format(rm, '.1f')
        lm = float(lm)
        rm = float(rm)
        self.pwm1.ChangeDutyCycle(lm)
        self.pwm2.ChangeDutyCycle(rm)
        time.sleep(0.08)

    #stop bot
    def stop(self):
        self.setPins(1, 1, 1, 1)
        self.setPWM(100.00, 100.00)
        self.anlaufboost = True

    #turn Jetbot on single point
    def turn(self, speed, direction):
        if (direction == "right"):
            self.setPins(1, 0, 0, 1)
        elif (direction == "left"):
            self.setPins(0, 1, 1, 0)

        self.setPWM(speed, speed)
        self.anlaufboost = False

    #turn Jetbot on single point with Gamepad Left Stick input
    def turnGamepad(self, ls):
        if (ls > self.con_thr):
            self.turn(self.aim_boost, "right")
        elif (ls < (-self.con_thr)):
            self.turn(self.aim_boost, "left")

    #drive forward/backwards with steering
    def drive(self, lm, rm, direction):
        if(direction == "forward"):
            self.setPins(1, 0, 1, 0)
        elif(direction == "backward"):
            self.setPins(0, 1, 0, 1)        
        self.setPWM(lm, rm)

    #calculate based on gamepad input the steering angele / velocity difference
    def calculateSteering(self, speed, ls):
        self.valpwm2 = speed * (100.0 - self.min_load) + self.min_load
        self.valpwm1 = self.valpwm2
        self.circle_act = self.circle_thr_min + (self.circle_thr_max - self.circle_thr_min) * speed

        if(ls < 0.00):
            ls = ls * (-1)
            self.valpwm2 = self.valpwm2 + self.circle_act * ls
            self.valpwm1 = self.valpwm1 - self.circle_act * ls

        elif(ls >= 0.00):
            self.valpwm1 = self.valpwm1 + self.circle_act * ls
            self.valpwm2 = self.valpwm2 - self.circle_act * ls

        if(self.valpwm1 > 100.00):
            self.valpwm2 = self.valpwm2 - (self.valpwm1 - 100.00)
            self.valpwm1 = 100.0
        elif(self.valpwm1 < self.min_load):
            self.valpwm2 = self.valpwm2 + (self.min_load - self.valpwm1)
            self.valpwm1 = self.min_load
        elif(self.valpwm2 > 100.00):
            self.valpwm1 = self.valpwm1 - (self.valpwm2 - 100.00)
            self.valpwm2 = 100.0
        elif(self.valpwm2 < self.min_load):
            self.valpwm1 = self.valpwm1 + (self.min_load - self.valpwm2)
            self.valpwm2 = self.min_load


        if(self.anlaufboost):
            self.anlaufboost = False
            self.valpwm1 = self.aim_boost
            self.valpwm2 = self.aim_boost

    def setSteering(self, speed, ls):
        self.calculateSteering(speed, ls)
        self.drive(self.valpwm1, self.valpwm2, "forward")

    #Control the JetBot with Gamepad-Input
    def gamepadcontroll(self, lt, rt, ls, ab, bb, xb, yb):
        #manage state wether velocity control is activated
        if(bb == 1):
            self.tempomat = False
            self.tem_val = 0
        elif(xb == 1):
            self.tempomat = True
        
        if(self.tempomat):
            #manage velocity of velocity control
            if(yb == 1) and (self.tem_val < 3):
                self.tem_val = self.tem_val + 1
            elif(ab == 1) and (self.tem_val > 0):
                self.tem_val = self.tem_val - 1
            print(self.tem_val)
            #apply velocity to motors
            #if speed is zero, allwo turn or stop
            if(self.tem_val == 0):
                if ((ls <= self.con_thr) or (ls>= (-self.con_thr))):
                    self.stop()
                else:
                    self.turnGamepad(ls)
            else:
                #define speed based on velocity control for drive and calculateSteering
                if(self.tem_val == 1):
                    self.tem_vel = 0.0
                elif(self.tem_val == 2):
                    self.tem_vel = 0.5
                elif(self.tem_val == 3):
                    self.tem_vel = 1
                    
                if(rt > self.tem_vel):
                    self.tem_vel = rt

                self.calculateSteering(self.tem_vel, ls)
                self.drive(self.valpwm1, self.valpwm2, "forward")
            
        elif(rt > 0.00) and (lt <= self.con_thr):
            self.calculateSteering(rt, ls)
            self.drive(self.valpwm1, self.valpwm2, "forward")
            
        elif(lt > 0.00) and (rt <= self.con_thr) and (not self.tempomat):
            self.calculateSteering(lt, ls)
            self.drive(self.valpwm1, self.valpwm2, "backward")

        elif (rt == 0.0) and (lt == 0.0) and ((ls >= self.con_thr) or (ls <= (-self.con_thr))):
            self.turnGamepad(ls)

        elif (rt <= self.con_thr) and (lt <= self.con_thr) and ((ls <= self.con_thr) or (ls>= (-self.con_thr)) and (not self.tempomat)):
            self.stop()