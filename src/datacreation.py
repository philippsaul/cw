#to use this .py execute from src folder

from controller.gamepad import Gamepad
from motor.motors import Motors
from video import web_streaming
from video.camera import Camera
import threading
import cv2

myGamepad = Gamepad()
myMopets = Motors()

myCam = Camera()

#start stram in background
stream_thread = threading.Thread(target=web_streaming.start)
stream_thread.start()

i = 0
j = 0

datei = open('./linedetection/data/textdatei.txt','w')

nimm_auf = False

try:
     while True:
          frame = myCam.getFrame()
          gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          kernel_size = 5
          blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

          low_threshold = 50
          high_threshold = 150
          edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
          
          web_streaming.video_frame = edges
          myGamepad.get_data()
          myMopets.gamepadcontroll(myGamepad.lt, myGamepad.rt, myGamepad.ls, myGamepad.ab, myGamepad.bb, myGamepad.xb, myGamepad.yb)

          if myGamepad.lb and nimm_auf:
               nimm_auf = False
          elif myGamepad.lb and not nimm_auf:
               nimm_auf = True
               i = 0
          print(nimm_auf)
     
          


          if i == 10 and nimm_auf:
               print("schreibe Daten")
               i = 0
               cv2.imwrite("./linedetection/data/pic_" + str(j) + ".jpg", edges)
               datei.write(str(j) + " " + str(myGamepad.ls) + "\n")
               print(str(j) + " " + str(myGamepad.ls) + "\n")
               j += 1
          else:
               i += 1
          
except:
     datei.close()

