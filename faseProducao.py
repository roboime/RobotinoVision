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

def findButtons(lowerBound, upperBound, img, arrayTotal, str):
	conts = findColor(lowerBound, upperBound)
	newConts = []

	for i in range(len(conts)):
		x,y,w,h = cv2.boundingRect(conts[i])
		if(w/h > 0.8 and w/h < 1.2):
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

#Print in file
def prin(st, state, file) :
	if(state == "Q"):
		file.write("QR: ")
	if(state == "V"):
		file.write("V: ")
	if(state == "P"):
		file.write("P: ")
	file.write(st)
	file.write("\n")
	return

#Main
if __name__ == '__main__':

	stateAI = "Q"
	nextState = "Q"
	stateImage = 0
	tries = 0
	file = open("RoboIME.txt", "w")
	#cam = cv2.VideoCapture(0)

	while(1):

			#CORES
			#Green
			lowerBoundGreen=np.array([67,95,20])
			upperBoundGreen=np.array([117,255,162])
			#Red
			lowerBoundRed=np.array([0,142,16])
			upperBoundRed=np.array([63, 225, 225])
			#Grey
			lowerBoundGrey = np.array([0,0,0])
			upperBoundGrey = np.array([179,255,152])

			#Pegar imagem e mostrar estado:
			imgName = "image_" + str(stateImage) + ".jpeg"
			img = cv2.imread(imgName)
			print(stateAI)

			#Ler QRCode e definir proximo estado
			if(stateAI == 'Q'):
				print("Procurando QRCode")
				qrCodes = decode(img)
				if(len(qrCodes) == 0):
					tries  = tries + 1
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

				#Find contours
				contours = findColor(lowerBoundGrey, upperBoundGrey)

				if(len(contours) == 0):
					print("Não achou a valvula")
					tries = tries + 1
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

			#Painel
			if(stateAI == 'P'):
				print("Procurando painel")

				arrayTotal = []
				contsGreen = findButtons(lowerBoundGreen, upperBoundGreen, img, arrayTotal, "D")
				contsRed = findButtons(lowerBoundRed, upperBoundRed, img, arrayTotal, "L")

				if(len(contsGreen) == 0 and len(contsRed) == 0):
					print("Nao achou o painel")
					tries = tries + 1
					continue

				print("Achou o painel")
				result = findAll(arrayTotal)
				prin(result, stateAI, file)
				nextState = "Q"

			
			#Parte final para todo caso(trocar de estado e comunicar com o robo)
			if(tries > 100):
				sys.end()
			if(stateAI != nextState):
				tries = 0
				stateAI = nextState
				stateImage += 1
				if(stateAI != 'Q' and stateAI != 'V' and stateAI != 'P'):
					stateAI = 'Q'
					nextState = "Q"
