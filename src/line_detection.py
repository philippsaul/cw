from controller.gamepad import Gamepad
from motor.motors import Motors
from video import web_streaming
from video.camera import Camera
import threading
import cv2 
import socket
import numpy as np

myGamepad = Gamepad()
myMopets = Motors()

myCam = Camera()

#start stram in background
stream_thread = threading.Thread(target=web_streaming.start)
stream_thread.start()

while True:
    frame = myCam.getFrame()

    
    # LINE DETECTION
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments
    line_image = np.copy(frame) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

    horizontal_threshold = 300 #600
    angles = []
    destinations = []
    destination_x = -1
    for line in lines:
        for x1, y1, x2, y2 in line:
            if y1 > horizontal_threshold or y2 > horizontal_threshold:
                if y2 > y1:
                    destination_x = x2
                else:
                    destination_x = x1
                destinations.append(destination_x)
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
    if not len(lines):
        destination_x = -1
    if not destination_x == -1:
        destination_x = np.average(destinations)
    
    angle = np.average(angles)    
    
    speed_factor = 0.5
    if destination_x == -1:
        angle_text = "stopp"
        myMopets.stop()
    else:
        lenk_faktor = (destination_x - 480)/ 480
    
    myMopets.setSteering(speed_factor*100, lenk_faktor)
   
    
    # cv2.putText(frame,angle_text,(50,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
    # cv2.putText(frame,str(destination_x),(50,180), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
    # frame = cv2.addWeighted(frame, 0.8, line_image, 10, 0)

    # line with pwm gpio motor run
    # pwm1.ChangeDutyCycle(100)
    # pwm2.ChangeDutyCycle(100)


    web_streaming.video_frame = frame
    myGamepad.get_data()
    myMopets.gamepadcontroll(myGamepad.lt, myGamepad.rt, myGamepad.ls, myGamepad.ab, myGamepad.bb, myGamepad.xb, myGamepad.yb)
