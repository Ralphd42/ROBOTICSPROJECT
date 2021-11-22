import cv2
import numpy as np 
import matplotlib.pyplot as plt
def nothing(x):
    pass

testimg ='sampSMall.jpg'

cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 20,255, nothing)
cv2.createTrackbar("LS", "Tracking", 120, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 120, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 49, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)
frame = cv2.imread(testimg)
while True:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lh = cv2.getTrackbarPos("LH", "Tracking")
    ls = cv2.getTrackbarPos("LS", "Tracking")
    lv = cv2.getTrackbarPos("LV", "Tracking")
    uh = cv2.getTrackbarPos("UH", "Tracking")
    us = cv2.getTrackbarPos("US", "Tracking")
    uv = cv2.getTrackbarPos("UV", "Tracking")
    hsvMin = np.array([lh, ls, lv])
    hsvMax = np.array([uh, us, uv])
    mask = cv2.inRange(hsv, hsvMin, hsvMax)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Show the result
    cv2.imshow("Result view", res)
    #print("loop")
    # Wait for the escape key to be pressed
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()