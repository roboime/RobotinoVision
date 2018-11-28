import numpy as np
import cv2

grey1 = np.uint8([[[33,31,32]]])
hsv_grey1 = cv2.cvtColor(grey1,cv2.COLOR_BGR2HSV)
print(hsv_grey1)
grey2 = np.uint8([[[80,80,80]]])
hsv_grey2 = cv2.cvtColor(grey2,cv2.COLOR_BGR2HSV)
print(hsv_grey2)