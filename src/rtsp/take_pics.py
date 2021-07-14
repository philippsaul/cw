import numpy as np
import cv2
import time

cap = cv2.VideoCapture('http://192.168.0.153:8000/')
i = 0

training = False # set to true for correct images, set to false for false images
if cap.isOpened():
        print("open")

while(True):
    # Capture frame-by-frame
    
    
    # cv2.imshow("test", frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):

    text = input("type in enter")  # or raw_input in python2
    if text == "":
        cap = cv2.VideoCapture('http://192.168.0.153:8000/')
        ret, frame = cap.read()
        if training:
            cv2.imwrite('./training_data_correct/pic_'+str(i)+'.jpg', frame)
            i = i + 1
        else:
            cv2.imwrite('./training_data_false/pic_'+str(i)+'.jpg', frame)
            i = i + 1
        cap.release()
    time.sleep(0.5)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()