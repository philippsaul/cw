import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
i = 0

training = False # set to true for correct images, set to false for false images

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if cap.isOpened():
        print("open")

    if training:
        cv2.imwrite('./training_data_correct/pic_'+str(i)+'.jpg', frame)
    else:
        cv2.imwrite('./training_data_false/pic_'+str(i)+'.jpg', frame)
    i = i + 1
    time.sleep(2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()