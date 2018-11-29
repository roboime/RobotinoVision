#https://www.learnopencv.com/barcode-and-qr-code-scanner-using-zbar-and-opencv/

from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

def decode(im) : 
  # Find QR code
  decodedObjects = pyzbar.decode(im)
 
  # Print results
  for obj in decodedObjects:
    objData = obj.data.decode("utf-8")
    print('Type : ', obj.type)
    print('Data : ', objData)
     
  return decodedObjects
 
 
# Main 
if __name__ == '__main__':
 
  # Read image
  im = cv2.imread('qr-imageValvula.jpg')
 
  decodedObjects = decode(im)