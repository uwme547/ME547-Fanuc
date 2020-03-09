import cv2 as cv2
import time
cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    cv2.imwrite("imgs/initial.png", frame)
    crop_y_init = 0
    crop_y_fin =  300
    crop_x_init = 60
    crop_x_fin = 560
    crop_img = frame[crop_y_init:crop_y_fin,crop_x_init:crop_x_fin]
    cv2.imwrite("imgs/cropped.png", crop_img)
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 75,255, cv2.THRESH_BINARY)
    cv2.imwrite("imgs/thresh.png", thresh)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("No of contours: " + str(len(contours)))

    cv2.drawContours(crop_img, contours,1, (0,255,0),3)
    cv2.imwrite("imgs/contour.png", crop_img)
    cnt = contours[1]
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    print("Centroid, cx: " + str(cx) + " , cy: " + str(cy))
    b = 2
    for x in range(-b,b):
        for y in range(-b,b):
            crop_img[cy+y,cx+x] = (0,0,255)

    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    for corner in box:
        for x in range(-b,b):
            for y in range(-b,b):
                crop_img[int(corner[1])+y,int(corner[0])+x] = (0,0,255)
        
    cv2.imwrite("imgs/points.png", crop_img)
    cv2.imshow('frame', crop_img)


    '''
    for(i in range(crop_y_init,crop_y_fin)):
        if ()


    '''
    cv2.waitKey(0)

cap.release()
