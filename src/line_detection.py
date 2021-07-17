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

try:
    myMopets.setPins(1,0,1,0)
    while True:
    
        frame = myCam.getFrame()


        alpha = 2
        beta = 1
        frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

        cv2.imwrite("pic.jpg", frame)
        # LINE DETECTION
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("gray.jpg", gray)
        
        kernel_size = 5
        blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
        

        low_threshold = 50
        high_threshold = 150
        edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
        cv2.imwrite("blur.jpg", edges)

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
        # print(lines)

        horizontal_threshold = 250 #600
        angles = []
        destinations = []
        destination_x = -1
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    if ((y2 - y1) / (x2 - x1) > 0.2 or (y2 - y1) / (x2 - x1) < -0.2) and (y1 > horizontal_threshold or y2 > horizontal_threshold):
                        destination_x = (horizontal_threshold - y2) * (x2 - x1) / (y2 - y1) + x2
                        print("Zielwert x: " + str(destination_x))
                        if destination_x > 0 and destination_x <= 980:
                            destinations.append(destination_x)
                    # if y1 > horizontal_threshold or y2 > horizontal_threshold:
                    #     if y2 > y1:
                    #         destination_x = x2
                    #     else:
                    #         destination_x = x1
                        
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 10)  
        print("for Schleife vorbei")                     
        if lines is None:
            destination_x = -1
        if not destination_x == -1:
            destination_x = np.average(destinations)   
        
        speed = 35.0
        print("nach speed = 35")
        lenk_faktor = abs((destination_x - 480)/ 480)
        print("roh lenkfaktor" + str(lenk_faktor))
        b = 0.25
        loss = b + lenk_faktor * 0.95

        
        # lenk_faktor = lenk_faktor * loss
        # lenk_faktor = lenk_faktor * (100.0 - speed) + speed
        # print("mit loss" + str(lenk_faktor))

        # if destination_x > 480:
        #     myMopets.setPWM( lenk_faktor, speed)
        # elif destination_x < 480:
        #     myMopets.setPWM(speed, lenk_faktor)
        # elif destination_x == 480:
        #     myMopets.setPWM(speed, speed)
        
    
        cv2.circle(frame,(int(destination_x),int(horizontal_threshold)), 20, (0,0,255), -1)
        # cv2.putText(frame,angle_text,(50,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame,str(destination_x),(50,180), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
        # frame = cv2.addWeighted(frame, 0.8, line_image, 10, 0)

        # line with pwm gpio motor run
        # pwm1.ChangeDutyCycle(100)
        # pwm2.ChangeDutyCycle(100)


        web_streaming.video_frame = frame
        # myGamepad.get_data()(myGamepad.lt, myGamepad.rt, myGamepad.ls, myGamepad.ab, myGamepad.bb, myGamepad.xb, myGamepad.yb)
except:
    print("Exception")
    myMopets.stop()
    # while True:
        # myGamepad.get_data()
        # myMopets.gamepadcontroll(myGamepad.lt, myGamepad.rt, myGamepad.ls, myGamepad.ab, myGamepad.bb, myGamepad.xb, myGamepad.yb)
