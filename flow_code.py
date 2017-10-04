import numpy as np
import cv2
import sys
import matplotlib
from calc_hist import * 

video = sys.argv[1]
folder = sys.argv[2]
#rotation = sys.argv[2]  #if a rotation is needed for the video, currently assumed to require a -90 degree rotation
#try
#	print rotation
#except

cap = cv2.VideoCapture(video)
print cap.isOpened()
# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (100,100),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
# Create some random colors
color = np.random.randint(0,255,(100,3))
# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)
count = 0
while(1):
    cap.read()
    ret,frame = cap.read()
    if str(frame) == "None":
    	break  #end of video
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # calculate optical flow

    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    # Select good points
    #print str(count) + " " + str(len(p1[st==1]))
    if len(p1[st==1]) != 0:
    	good_new = p1[st==1]  # had to add the if for this in the case that there are no good pts
    good_old = p0[st==1]
    # draw the tracks
    
    binL = 0	#init bins
    binR = 0
    bin = [0]*2
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
	bin = compute(bin,a-c,b-d)
	if d-b > 0:	# if the old x-component point > new, movement of camera to left
		binL += 1
	else:
		binR += 1
        cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
    createHistogram(bin,count, folder)
    img = cv2.add(frame,mask)
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)
    # rotate the image by -90 degrees
    M = cv2.getRotationMatrix2D(center, -90, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))
    cv2.imshow('frame',rotated)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    mask = np.zeros_like(frame)
    count += 1
cap.release()
