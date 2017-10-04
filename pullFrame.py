import numpy as np
import cv2
import sys
import matplotlib
from calc_hist import * 

filename = sys.argv[1]
frame = sys.argv[2]
#print frame
cap = cv2.VideoCapture(filename)
vid_length = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
#print cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, float(frame))
#print cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
#for x in range(int(frame)):
	#cap.read()	#read all the undesirable previous frames
ret, frame = cap.read() #get the desired frame
cv2.imshow('frame',frame)
k = cv2.waitKey(10000) & 0xff

