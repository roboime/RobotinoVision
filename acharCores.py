#https://thecodacus.com/opencv-object-tracking-colour-detection-python/#.W_50ZqeZOgQ

import cv2
import numpy as np
from matplotlib import pyplot as plt

def nothing(x):
	pass

#Main
if __name__ == '__main__':
	# named ites for easy reference
	barsWindow = 'Bars'
	hl = 'H Low'
	hh = 'H High'
	sl = 'S Low'
	sh = 'S High'
	vl = 'V Low'
	vh = 'V High'

	# create window for the slidebars
	cv2.namedWindow(barsWindow, flags = cv2.WINDOW_AUTOSIZE)

	# create the sliders
	cv2.createTrackbar(hl, barsWindow, 0, 179, nothing)
	cv2.createTrackbar(hh, barsWindow, 0, 179, nothing)
	cv2.createTrackbar(sl, barsWindow, 0, 255, nothing)
	cv2.createTrackbar(sh, barsWindow, 0, 255, nothing)
	cv2.createTrackbar(vl, barsWindow, 0, 255, nothing)
	cv2.createTrackbar(vh, barsWindow, 0, 255, nothing)

	# set initial values for sliders
	cv2.setTrackbarPos(hl, barsWindow, 0)
	cv2.setTrackbarPos(hh, barsWindow, 179)
	cv2.setTrackbarPos(sl, barsWindow, 0)
	cv2.setTrackbarPos(sh, barsWindow, 255)
	cv2.setTrackbarPos(vl, barsWindow, 0)
	cv2.setTrackbarPos(vh, barsWindow, 255)

	while(True):
		frame = cv2.imread('valvula6.jpeg')
		frame = cv2.GaussianBlur(frame, (5, 5), 0)
    
    	# convert to HSV from BGR
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    	# read trackbar positions for all
		hul = cv2.getTrackbarPos(hl, barsWindow)
		huh = cv2.getTrackbarPos(hh, barsWindow)
		sal = cv2.getTrackbarPos(sl, barsWindow)
		sah = cv2.getTrackbarPos(sh, barsWindow)
		val = cv2.getTrackbarPos(vl, barsWindow)
		vah = cv2.getTrackbarPos(vh, barsWindow)

    	# make array for final values
		HSVLOW = np.array([hul, sal, val])
		HSVHIGH = np.array([huh, sah, vah])

    	# apply the range on a mask
		mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
		maskedFrame = cv2.bitwise_and(frame, frame, mask = mask)

		# display the camera and masked images
		cv2.imshow('Masked', maskedFrame)
		cv2.imshow('Camera', frame)

		# check for q to quit program with 5ms delay
		if cv2.waitKey(5) & 0xFF == ord('q'):
			break

	# clean up our resources
	cap.release()
	cv2.destroyAllWindows()