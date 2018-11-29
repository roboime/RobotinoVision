from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Find QR code
def decode(im) : 
  decodedObjects = pyzbar.decode(im)     
  return decodedObjects

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

#Print in file
def prin(st, state, file) :
	if(state == "Q"):
		file.write("QR: ")
	if(state == "V"):
		file.write("V: ")
	file.write(st)
	file.write("\n")
	return

#Main
if __name__ == '__main__':

	stateAI = "Q"
	nextState = "Q"
	stateImage = 0
	file = open("RoboIME.txt", "w")
	#cam = cv2.VideoCapture(0)

	while(1):

			#Pegar imagem e mostrar estado:
			imgName = "image_" + str(stateImage) + ".jpg"
			img = cv2.imread(imgName)
			print(stateAI)

			#Ler QRCode e definir proximo estado
			if(stateAI == 'Q'):
				print("Procurando QRCode")
				qrCodes = decode(img)
				if(len(qrCodes) == 0):
					print("Nao achou QRCode\n")
					continue
				qr = qrCodes[0]
				data = qr.data.decode("utf-8")
				print("Achou QRCode", data)
				prin(data, stateAI, file)
				nextState = data[0]

			#Valvula
			if(stateAI == "V"):
				print("Procurando a valvula")

				#Color grey definition
				lowerBound = np.array([0,0,0])
				upperBound = np.array([70,98,77])
				#Find contours
				contours = findColor(lowerBound, upperBound)

				if(len(contours) == 0):
					print("Não achou a valvula")
					continue
				print("Achou a valvula")

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
					prin("A", stateAI, file)
				else:
					prin("F", stateAI, file)
				nextState = 'Q'

			
			#Parte final para todo caso(trocar de estado e comunicar com o robo)
			if(stateAI != nextState):
				stateAI = nextState
				stateImage += 1
				if(stateAI != 'Q' and stateAI != 'V'):
					stateAI = 'Q'
					nextState = "Q"
