from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Find QR code
def decode(im) : 
  decodedObjects = pyzbar.decode(im)     
  return decodedObjects

#Print in file
def prin(st, stateAI) :
	if(stateAI == "Q"):
		file.write("QR: ")
	if(stateAI == "V"):
		file.write("V: ")
	file.write(st)
	file.write("\n")
	return


#Find the contours of selected color
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

#Main
if __name__ == '__main__':

	stateAI = "V"
	nextState = "V"
	file = open("RoboIME.txt", "w")
	#cam = cv2.VideoCapture(0)

	while(1):

		status = input()
		#ret, img = cam.read()
		#cv2.imshow("cam", img)

		#Loop de estados
		if(status == ' '):

			#Pegar imagem e mostrar estado:
			img = cv2.imread("image.jpg")
			print(stateAI)

			#Ler QRCode e definir proximo estado
			if(stateAI == 'Q'):
				qrCodes = decode(img)
				if(len(qrCodes) == 0):
					print("Nao achou QRCode\n")
					continue
				qr = qrCodes[0]
				data = qr.data.decode("utf-8")
				prin(data, stateAI)
				nextState = data[0]

			#Valvula
			if(stateAI == "V"):
				#Color grey definition
				lowerBound = np.array([0,0,0])
				upperBound = np.array([70,98,77])
				#Find contours
				contours = findColor(lowerBound, upperBound)

				#Find biggest rectangle
				rect = None
				area = 0.0
				for i in range(len(contours)):
					x,y,w,h = cv2.boundingRect(contours[i])
					if(area < w*h):
						rect = contours[i]
						area = w*h

				x,y,w,h = cv2.boundingRect(rect)

				#Define if valvula is open or not e definir proximo estado
				if(h/w > 1.3):
					prin("A", stateAI)
				else:
					prin("F", stateAI)
				nextState = 'Q'

			
			#Parte final para todo caso(trocar de estado e comunicar com o robo)
			if(stateAI != nextState):
				stateAI = nextState
				if(stateAI != 'Q' or stateAI != 'V'):
					stateAI = 'Q'
					nextState = "Q"

		else:
			sys.exit()