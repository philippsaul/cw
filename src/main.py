
import threading
import time

import Jetson.GPIO as GPIO

from calculate_steering_data.calculate_steering_data import \
    Calculate_steering_data
from controller.gamepad import Gamepad
from driving.main_driving import Drivetrain
from log import log
from safety.safety import Safety
from video import web_streaming
from video.camera import Camera
from video import web_streaming

motor_output_enable_pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(motor_output_enable_pin, GPIO.OUT, initial = GPIO.HIGH) # disables output


mylog = log()
mylog.info('STARTING!')
# myCam = Camera()
myGamepad = Gamepad(log = mylog)
myDrivetrain = Drivetrain(log = mylog, gpio = GPIO, output_enable_pin = motor_output_enable_pin)
mySafety = Safety(log = mylog, gamepad = myGamepad)
myCalcSteering = Calculate_steering_data(log = mylog, gamepad = myGamepad)

# start stram in background
stream_thread = threading.Thread(target=web_streaming.start)
stream_thread.start()


try:
     mySafety.enable_gamepad()

     while not mylog.error:
          # frame = myCam.getFrame()
          # web_streaming.video_frame = frame

          myGamepad.get_data()
          mySafety.safety()
          steering_data = myCalcSteering.calc()
          myDrivetrain.drive(steering_data)

          # print(myDrivetrain.myBLDC.myAS5600.avg_speed(0), end='              \r')
          # print('{:2.1f} | {:2.1f} | {:2.1f}'.format(myDrivetrain.myBLDC.myAS5600.rotation_difference()[0], myDrivetrain.myBLDC.myAS5600.rotation_difference()[1], myDrivetrain.myBLDC.myAS5600.rotation_difference()[2]), end='              \r') # debugging


# 'except Exception as e:' does not stop the motors
except:
     myDrivetrain.__del__()
     GPIO.cleanup()
     mylog.warning('STOPPED!')
