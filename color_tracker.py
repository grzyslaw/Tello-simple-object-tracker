import cv2
import numpy as np

def detect_and_mark_red(frame):
    
    object_center = None

    #convert frame to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # #define range of red
    # lower_red1 = np.array([0, 70, 50])
    # upper_red1 = np.array([10, 255, 255])++

    # lower_red2 = np.array([160, 70, 50])
    # upper_red2 = np.array([180, 255, 255])

    # mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    # mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    # red_mask = cv2.bitwise_or(mask1, mask2)

    #red pillow but considered blue by camera xd
    lower_target = np.array([110, 100, 100])
    upper_target = np.array([125, 255, 255])
    mask = cv2.inRange(hsv_frame, lower_target, upper_target)

    area = 0
    #draw rect on detected red area
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        #remove the noise
        if area > 10000:
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)
            object_center = (x + w // 2, y + h // 2)
            frame = cv2.circle(frame, object_center, 3, (0,0,255), 2)
            break

    if object_center is None:
        object_center = (-1,-1)

    return frame, mask, object_center, area, hsv_frame
    
