# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time


def ball_detection():
	# vs = VideoStream(0, cv2.CAP_V4L2).start()
	vs = cv2.VideoCapture(0)
	# allow the camera or video file to warm up
	time.sleep(2.0)

	# keep looping

	try:
		# grab the current frame
		_, frame = vs.read()
		# handle the frame from VideoCapture or VideoStream
		frame = frame
		# if we are viewing a video and we did not grab a frame,
		# then we have reached the end of the video
		# if frame is None:
		# 	break
		# resize the frame, blur it, and convert it to the HSV
		# color space
		frame = imutils.resize(frame, width=600)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
		# cv2.imshow("Frame", hsv)
		# construct a mask for the color "green", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask

		hsv_redLower = np.array([160, 83, 100])
		hsv_redUpper = np.array([180, 255, 255])
		# hsv_redLower = np.array([160])
		# hsv_redUpper = np.array([180])

		mask = cv2.inRange(hsv, hsv_redLower, hsv_redUpper)
		# cv2.imshow("Frame", mask)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)



		# find contours in the mask and initialize the current
		# (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		center = None
		# only proceed if at least one contour was found
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			# only proceed if the radius meets a minimum size
			if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
				cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
			# cv2.imshow("Frame", frame)
			# key = cv2.waitKey(1) & 0xFF
			# if the 'q' key is pressed, stop the loop
			# if key == ord("q"):
			# 	break
			return (x-frame.shape[1]/2)/(frame.shape[1]/2), 0.4
		return (0, 0)
	except Exception as e:
		print(e)



		
        