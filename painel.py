from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
from matplotlib import pyplot as plt

def findColor(lowerBound, upperBound):
	font = cv2.FONT_HERSHEY_SIMPLEX
	imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(imgHSV,lowerBound,upperBound)
	kernelOpen = np.ones((5,5))
	kernelClose = np.ones((20,20))
	maskOpen = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
	maskClose = cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
	_, conts, h = cv2.findContours(maskClose.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	return conts

def findButtons(lowerBound, upperBound, img, arrayTotal, str):
	conts = findColor(lowerBound, upperBound)
	newConts = []

	for i in range(len(conts)):
		x,y,w,h = cv2.boundingRect(conts[i])
		if(w/h > 0.7 and w/h < 1.3):
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
			newConts.append(conts[i])
			arrayTotal.append([x, str])

	return newConts

def findAll(arrayTotal):
	bubbleSort(arrayTotal)
	result = ""
	for i in range(len(arrayTotal)):
		result = result + arrayTotal[i][1]
	return result

def bubbleSort(arr):
	n = len(arr)
	for i in range(n):
		for j in range(0, n-i-1):
			if arr[j][0] > arr[j+1][0] :
				arr[j], arr[j+1] = arr[j+1], arr[j]

def findInArray(value, contArray, str):
	for i in range(len(contArray)):
		x,y,w,h = cv2.boundingRect(contArray[i])
		x1,y1,w1,h1 = cv2.boundingRect(value)
		if(x == x1 and y == y1 and w == w1 and h == h1):
			return str
	return ""


#Main
if __name__ == '__main__':
	imgName = "image_3.jpeg"
	img = cv2.imread(imgName)

	#Define green
	lowerBoundGreen=np.array([95,91,0])
	upperBoundGreen=np.array([118,255,154])

	#Define red
	lowerBoundRed=np.array([0,153,204])
	upperBoundRed=np.array([179,235,255])

	arrayTotal = []
	contsGreen = findButtons(lowerBoundGreen, upperBoundGreen, img, arrayTotal, "D")
	contsRed = findButtons(lowerBoundRed, upperBoundRed, img, arrayTotal, "L")

	result = findAll(arrayTotal)
	print(result)

	cv2.imshow("image", img)
	cv2.waitKey(0)

