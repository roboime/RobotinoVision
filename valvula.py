#https://thecodacus.com/opencv-object-tracking-colour-detection-python/#.W_50ZqeZOgQ

import cv2
import numpy as np
from matplotlib import pyplot as plt

def nothing(x):
	pass

#Main
if __name__ == '__main__':

	#Definicao das cores
	#lowerBound=np.array([0,0,0])
	#upperBound=np.array([70,98,77])
	lowerBound = np.array([95,91,0])
	upperBound = np.array([118,255,154])

	#Create font to print on screen
	font = cv2.FONT_HERSHEY_SIMPLEX

	#Choose foto and resize
	img = cv2.imread('image_3.jpeg')
	#img = cv2.resize(imgBig, (340,220))

	#Convert image to HSV format
	imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	#Create a mask for the desired color
	mask = cv2.inRange(imgHSV,lowerBound,upperBound)

	#Control the random dots that appear in the mask
	kernelOpen = np.ones((5,5))
	kernelClose = np.ones((20,20))
	maskOpen = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
	maskClose = cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

	#Pick the mask with the least amount of noise and find the contours of the object
	_, conts, h = cv2.findContours(maskClose.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

	#Pick the biggest rectangle 
	rect = None
	area = 0.0
	for i in range(len(conts)):
		x,y,w,h = cv2.boundingRect(conts[i])
		cv2.drawContours(img,conts[i],-1,(255,0,0),3)
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
		if(area < w*h):
			rect = conts[i]
			area = w*h

	#x,y,w,h = cv2.boundingRect(rect)
	#cv2.drawContours(img,rect,-1,(255,0,0),3)
	#cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
	if(h/w > 1.3):
		print("Aberto")
	else:
		print("Fechado")
	cv2.imshow("image_1", img)
	cv2.waitKey(0)