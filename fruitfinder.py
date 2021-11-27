import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('samp.jpg')#, cv2.IMREAD_GRAYSCALE)
imghsv =cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

#use threshholds from blob2.py
# these can change
# create a mask
thMask =  cv2.inRange(imghsv, (56,179,120),(195,255,255))
thMask = cv2.erode(thMask, None, iterations=3)
thMask = cv2.dilate(thMask, None, iterations=3)
prms = cv2.SimpleBlobDetector_Params()
prms.minThreshold = 0 
prms.maxThreshold = 100 
 
# Filter by Area.
prms.filterByArea = True
prms.minArea = 400
prms.maxArea = 20000
 
# Filter by Circularity
prms.filterByCircularity = False
prms.minCircularity = 0.1
 
# Filter by Convexity
prms.filterByConvexity = False
prms.minConvexity = 0.5
 
# Filter by Inertia
prms.filterByInertia = False
prms.minInertiaRatio = 0.5

# Detect blobs
detector = cv2.SimpleBlobDetector_create(prms)




 

keypoints = detector.detect(255-thMask)
#detector = cv2.SimpleBlobDetector()
 
print(keypoints)

for kp in keypoints:
    print (kp.pt)
    x,y = kp.pt
    print ("x{},y{}" ,x,y )
# Detect blobs.
 
#keypoints = detector.detect(img)
 
 

# Draw detected blobs as red circles.
 
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
 
 
 
# Show keypoints



 
im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("Keypoints", im_with_keypoints)
 
cv2.waitKey(0)
cv2.destroyAllWindows()











cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()