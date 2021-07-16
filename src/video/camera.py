import os
import cv2

class Camera:
    def __init__(self):
        self.GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12, framerate=59/1 ! nvvidconv flip-method=2 ! video/x-raw, width=960, height=616, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink wait-on-eos=false max-buffers=1 drop=True'
        self.open()

    def __del__ (self):
        self.close()

    def open(self):
        os.system("sudo systemctl restart nvargus-daemon")
        self.video_capture = cv2.VideoCapture(self.GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)

    def getFrame(self):
        if self.video_capture.isOpened():
            self.return_key, self.frame = self.video_capture.read()
            if not self.return_key:
                return -1
            # cv2.imwrite("test.jpg", self.frame)
            return self.frame

    def close(self):
        self.video_capture.release()
    