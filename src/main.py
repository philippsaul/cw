
import threading
import time

from calculate_steering_data.calculate_steering_data import \
    Calculate_steering_data
from controller.gamepad import Gamepad
from driving.main_driving import Drivetrain
from log import log
from motor.motors import Motors  # old brushed motors
from safety.safety import Safety
from video import web_streaming
from video.camera import Camera

# myCam = Camera()
myGamepad = Gamepad()
myDrivetrain = Drivetrain()
myMopets = Motors() # old brushed motors
mySafety = Safety(gamepad = myGamepad)
myCalcSteering = Calculate_steering_data(gamepad = myGamepad)

mySafety.enable_gamepad()

#start stram in background
# stream_thread = threading.Thread(target=web_streaming.start)
# stream_thread.start()

while True:
     try:
          # frame = myCam.getFrame()
          # web_streaming.video_frame = frame

          # myGamepad.get_data()
          # myMopets.gamepadcontroll(myGamepad.lt, myGamepad.rt, myGamepad.ls, myGamepad.ab, myGamepad.bb, myGamepad.xb, myGamepad.yb)


          myGamepad.get_data()
          # print(myGamepad.xb)
          # mySafety.safety() # empty
          steering_data = myCalcSteering.calc()
          # if myGamepad.xb:
          #      steering_data = (1, 0)
          # else:
          #      steering_data = (0, 0)
          steering_data = (1, 0)
          time.sleep(0.0001)
          myDrivetrain.drive(steering_data)
          # print(myDrivetrain.myBLDC.myAS5600.avg_speed(0), end='              \r')
          # print('{:2.1f} | {:2.1f} | {:2.1f}'.format(myDrivetrain.myBLDC.myAS5600.rotation_difference()[0], myDrivetrain.myBLDC.myAS5600.rotation_difference()[1], myDrivetrain.myBLDC.myAS5600.rotation_difference()[2]), end='              \r') # debugging
     except Exception as e:
          log.error(e)
          raise Exception(e)



