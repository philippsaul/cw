import Jetson.GPIO as GPIO
import time
import threading
import configparser
import socket


class Motors:
    def __init__(self):
        #definition of motor control pins on Jetson Nano
        self.pin_pwm_motor_rechts = 32
        self.pin_pwm_motor_links = 33
        self.pin_motor_rechts_richtung = 35
        self.pin_motor_links_richtung = 36

        # self.pwm_previous_value_left = 0
        # self.pwm_previous_value_right = 0
        self.pwm_value_left = 0
        self.pwm_value_right = 0
        self.pwm1= 0
        self.pwm2 = 0

        self.max_speed = 0
        # self.max_acc = 0
        self.con_thr = 0
        self.con_str = 0


        self.config = configparser.ConfigParser()
        self.config.read('./settings.ini')
        
        for section in self.config.sections():
            if self.config[section]['hostname'] == socket.gethostname():
                self.section = self.config[section]
                break
        if self.section == None:
            raise Exception("can't find hostname in settings.ini")

        self.max_speed = float(self.section["max_speed"])
        # self.max_acc = float(self.section["max_acc"])
        self.con_thr = float(self.section["deadzone_throttle"])
        self.con_str = float(self.section["deadzone_stearing"])

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.pin_pwm_motor_rechts, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pin_pwm_motor_links, GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.pin_motor_rechts_richtung, GPIO.OUT, initial=GPIO.LOW)       #setup direction status
        GPIO.setup(self.pin_motor_links_richtung, GPIO.OUT, initial=GPIO.LOW)       #setup direction status
        self.pwm1 = GPIO.PWM(self.pin_pwm_motor_rechts, 100)
        self.pwm2 = GPIO.PWM(self.pin_pwm_motor_links, 100)

        #start pwm session
        self.pwm1.start(self.pwm_value_left)
        self.pwm2.start(self.pwm_value_right)

    #clean up the GPIOs and PWM session
    def clean (self):
        self.pwm1.stop()
        self.pwm2.stop()
        GPIO.cleanup()

    def __del__ (self):
        self.clean()
    



    #Base function for setting PWM Pins to targeted value
    def setPWM(self, left_motor, right_motor):
        left_motor = format(left_motor, '.1f')  
        right_motor = format(right_motor, '.1f')
        left_motor = float(left_motor)
        right_motor = float(right_motor)

        if (left_motor <= 100.0) and (left_motor >= 0.0):
            self.pwm1.ChangeDutyCycle(left_motor)
        else:
            self.pwm1.ChangeDutyCycle(0)
            self.pwm2.ChangeDutyCycle(0)
            raise Exception('PWM1 value out of range')

        if (right_motor <= 100.0) and (right_motor >= 0.0):
            self.pwm2.ChangeDutyCycle(right_motor)
        else:
            self.pwm1.ChangeDutyCycle(0)
            self.pwm2.ChangeDutyCycle(0)
            raise Exception('PWM2 value out of range')


    def drive(self, trigger_diff, ls):
        # calculate speed
        self.pwm_value_left = self.max_speed * trigger_diff + (self.max_speed/5) * ls
        self.pwm_value_right = self.max_speed * trigger_diff - (self.max_speed/5) * ls

        # maximaize speed
        if(self.pwm_value_left > self.max_speed):
            self.pwm_value_left = self.max_speed
        elif(self.pwm_value_left < (-self.max_speed)):
            self.pwm_value_left = -self.max_speed

        if(self.pwm_value_right > self.max_speed):
            self.pwm_value_right = self.max_speed
        elif(self.pwm_value_right < (-self.max_speed)):
            self.pwm_value_right = -self.max_speed

        # set directions, right left has changed because driving direction changed
        if(self.pwm_value_left >= 0):
            GPIO.output(self.pin_motor_rechts_richtung, GPIO.LOW)
        else:
            GPIO.output(self.pin_motor_rechts_richtung, GPIO.HIGH)
        if(self.pwm_value_right >= 0):
            GPIO.output(self.pin_motor_links_richtung, GPIO.HIGH)
        else:
            GPIO.output(self.pin_motor_links_richtung, GPIO.LOW)


    #Control the JetBot with Gamepad-Input
    def gamepadcontroll(self, lt, rt, ls, ab, bb, xb, yb):

        trigger_diff = rt - lt

        if (trigger_diff > self.con_thr) or (trigger_diff < (-self.con_thr)) or (ls > self.con_str) or (ls < (-self.con_str)):
            self.drive(trigger_diff, ls)

        else:
            self.pwm_value_right = 0.0
            self.pwm_value_left = 0.0
        
        self.setPWM(abs(self.pwm_value_left), abs(self.pwm_value_right))
        print('PWM_R: {:.2f} \t PWM_L: {:.2f}'.format(self.pwm_value_right ,self.pwm_value_left ))
        time.sleep(0.1)
        

            
