from controller.gamepad import Gamepad
from motor.motors import Motors
from video import web_streaming
from video.camera import Camera
import threading

myGamepad = Gamepad()
myMopets = Motors()

myCam = Camera()

#start stram in background
stream_thread = threading.Thread(target=web_streaming.start)
stream_thread.start()

while True:
     frame = myCam.getFrame()
     
     web_streaming.video_frame = frame
     myGamepad.get_data()
     myMopets.gamepadcontroll(myGamepad.lt, myGamepad.rt, myGamepad.ls, myGamepad.ab, myGamepad.bb, myGamepad.xb, myGamepad.yb)
