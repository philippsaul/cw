import cv2
import time
import threading
from flask import Response, Flask
import os
import socket
import numpy as np
import math
import Jetson.GPIO as GPIO

os.system("sudo systemctl restart nvargus-daemon")

activate_menu = False
menu_content = ["Ball Jagen", "Mario Kart", "Tore fahren", "Settings", "back"]
menu_images = ["../../assets/background_menu.jpg","../../assets/background_menu.jpg","../../assets/background_menu.jpg","../../assets/background_menu.jpg","../../assets/background_menu.jpg"]
active_menu_item = 2

# Image frame sent to the Flask object
global video_frame
video_frame = None

# Use locks for thread-safe viewing of frames in multiple browsers
global thread_lock 
thread_lock = threading.Lock()

# GStreamer Pipeline to access the Raspberry Pi camera
GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12, framerate=59/1 ! nvvidconv flip-method=2 ! video/x-raw, width=960, height=616, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink wait-on-eos=false max-buffers=1 drop=True'

# Create the Flask object for the application
app = Flask(__name__)

# GPIO SETUP
pwm_pin_motor_rechts = 32
pwm_pin_motor_links = 33
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(pwm_pin_motor_rechts, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pwm_pin_motor_links, GPIO.OUT,initial=GPIO.LOW)
pwm1 = GPIO.PWM(pwm_pin_motor_rechts, 100)
pwm2 = GPIO.PWM(pwm_pin_motor_links, 100)
valpwm1 = 0
valpwm2 = 0
pwm1.start(valpwm1)
pwm2.start(valpwm2)




def captureFrames():
    global video_frame, thread_lock

    # Video capturing from OpenCV
    video_capture = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)

    last_timestamp = time.time()

    while True and video_capture.isOpened():
        return_key, frame = video_capture.read()

        ################################################################
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Hostname 
        # cv2.putText(frame,socket.gethostname(),(300,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

        # Platzierung
        # if not activate_menu:
        #     if socket.gethostname() == "nanolars" or socket.gethostname() == "nanop":
        #         cv2.putText(frame,"1.",(10,550), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 2, cv2.LINE_AA)
        #     else:
        #         cv2.putText(frame,"4.",(10,550), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 2, cv2.LINE_AA)

        if activate_menu:
            frame = menu(frame)
        

        # # FACE DETECTION
        # face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # # Convert into grayscale
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # # Detect faces
        # faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # # Draw rectangle around the faces
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)







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
        # destinations = []
        # destination_x = -1
        # for line in lines:
        #     for x1, y1, x2, y2 in line:
        #         if y1 > horizontal_threshold or y2 > horizontal_threshold:
        #             if y2 > y1:
        #                 destination_x = x2
        #             else:
        #                 destination_x = x1
        #             destinations.append(destination_x)
        #             cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        # if not len(lines):
        #     destination_x = -1
        # if not destination_x == -1:
        #     destination_x = np.average(destinations)
        
        # angle = np.average(angles)    
        
        # speed_factor = 0.35
        # if destination_x == -1:
        #     angle_text = "stopp"
        #     pwm1.ChangeDutyCycle(0.0)
        #     pwm2.ChangeDutyCycle(0.0)


        # elif destination_x < 540 and destination_x > 420:
        #     angle_text = "gerade aus"
        #     pwm1.ChangeDutyCycle(speed_factor*100.0)
        #     pwm2.ChangeDutyCycle(speed_factor*100.0)


        # elif destination_x > 540:
        #     # ganz rechts ist weitester Ausschlag, wird erreicht durch größte pwm Differenz
        #     lenk_faktor = (destination_x-540) / (960-540)
        #     lenk_faktor = 1- lenk_faktor+0.3
        #     angle_text = "rechts"
        #     pwm1.ChangeDutyCycle(speed_factor*100.0)
        #     pwm2.ChangeDutyCycle(speed_factor*100.0*lenk_faktor)
        


        # elif destination_x < 420:
        #     lenk_faktor = destination_x / 420
        #     lenk_faktor = lenk_faktor + 0.3
        #     angle_text = "links"
        #     pwm1.ChangeDutyCycle(speed_factor*100.0*lenk_faktor)
        #     pwm2.ChangeDutyCycle(speed_factor*100.0)
       


        # else: 
        #     angle_text = "error"
        #     pwm1.ChangeDutyCycle(0)
        #     pwm2.ChangeDutyCycle(0)

        # speed_factor = 0
        # if angle < 5.0 and angle > -5.0:
        #     angle_text = "gerade aus"
        #     pwm1.ChangeDutyCycle(speed_factor*100.0)
        #     pwm2.ChangeDutyCycle(speed_factor*100.0)
        # elif angle > 5.0 and angle < 20.0:
        #     angle_text = "bisschen rechts"
        #     pwm1.ChangeDutyCycle(speed_factor*80.0)
        #     pwm2.ChangeDutyCycle(speed_factor*100.0)
        # elif angle > 20.0:
        #     angle_text = "stark rechts"
        #     pwm1.ChangeDutyCycle(speed_factor*60.0)
        #     pwm2.ChangeDutyCycle(speed_factor*100.0)
        # elif angle < -5.0 and angle > -20.0:
        #     angle_text = "bisschen links"
        #     pwm1.ChangeDutyCycle(speed_factor*100.0)
        #     pwm2.ChangeDutyCycle(speed_factor*80.0)
        # elif angle < -20.0:
        #     angle_text = "stark links"
        #     pwm1.ChangeDutyCycle(speed_factor*100.0)
        #     pwm2.ChangeDutyCycle(speed_factor*60.0)
        # else: 
        #     angle_text = "error"
        #     pwm1.ChangeDutyCycle(0)
        #     pwm2.ChangeDutyCycle(0)

        
        
        # cv2.putText(frame,angle_text,(50,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
        # cv2.putText(frame,str(destination_x),(50,180), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)

        
        # time measurement
        # timestamp = time.time()
        
        # cv2.putText(frame,str(1/(timestamp - last_timestamp)),(50,180), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
        # frame = cv2.addWeighted(frame, 0.8, line_image, 10, 0)
        # last_timestamp = timestamp


        # line with pwm gpio motor run
        # pwm1.ChangeDutyCycle(100)
        # pwm2.ChangeDutyCycle(100)







        ################################################################
       
        if not return_key:
            break

        # Create a copy of the frame and store it in the global variable,
        # with thread safe access
        with thread_lock:
            video_frame = frame.copy()
        
        key = cv2.waitKey(30) & 0xff
        if key == 27:
            break

    video_capture.release()


def menu(frame):
    return frame    
    # frame = np.zeros((616, 960, 3), dtype = "uint8")

    shape_multiplier = 1.5
    frame = cv2.imread(menu_images[active_menu_item])
    for i in range(len(menu_content)):
        if active_menu_item == i:      
            
            # print(menu_content)

            if menu_content[i] == "back":
                cv2.putText(frame,menu_content[i],(750,500), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
            else:             
                
                # shape around menu item
                pts = np.array([[40,(i+1)*100-20],[20,(i+1)*100],[40, (i+1)*100+20],[shape_multiplier*200, (i+1)*100+20],[shape_multiplier*200+20, (i+1)*100],[shape_multiplier*200, (i+1)*100-20]], np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.fillPoly(frame, [pts], (100,100,100))

                cv2.putText(frame,menu_content[i],(50,(i+1)*100+12), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)

        else:
            if menu_content[i] == "back":
                
                cv2.putText(frame,menu_content[i],(750,500), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
            else:
                
                # shape around menu item
                pts = np.array([[40,(i+1)*100-20],[20,(i+1)*100],[40, (i+1)*100+20],[shape_multiplier*200, (i+1)*100+20],[shape_multiplier*200+20, (i+1)*100],[shape_multiplier*200, (i+1)*100-20]], np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.fillPoly(frame, [pts], (100,100,100))

                cv2.putText(frame,menu_content[i],(50,(i+1)*100+12), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
    return frame

        
def encodeFrame():
    global thread_lock
    while True:
        # Acquire thread_lock to access the global video_frame object
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue
            return_key, encoded_image = cv2.imencode(".jpg", video_frame)
            if not return_key:
                continue

        # Output image as a byte array
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encoded_image) + b'\r\n')

@app.route("/")
def streamFrames():
    return Response(encodeFrame(), mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':

    # Create a thread and attach the method that captures the image frames, to it
    process_thread = threading.Thread(target=captureFrames)
    process_thread.daemon = True

    # Start the thread
    process_thread.start()

    # start the Flask Web Application
    # While it can be run on any feasible IP, IP = 0.0.0.0 renders the web app on
    # the host machine's localhost and is discoverable by other machines on the same network 
    app.run("0.0.0.0", port="8000")
