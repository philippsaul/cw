
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
          # mySafety.safety() # empty
          steering_data = myCalcSteering.calc()
          myDrivetrain.drive(steering_data)
     except Exception as e:
          log.error(e)
          raise Exception(e)



