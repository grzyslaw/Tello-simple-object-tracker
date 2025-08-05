from djitellopy import Tello
import cv2
from tracker import detect_and_mark_red
from control import adjust_drone_position
import time

# function to debug color manualy
# example usage cv2.setMouseCallback("Tracker output", show_hsv_values, hsv_frame)
def show_hsv_values(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        hsv_val = param[y, x]  # row = y, column = x
        print(f"HSV @ ({x},{y}): {hsv_val}")

def main(): 
    #initialize tello
    drone = Tello()

    #connect tello and start stream
    drone.connect()
    print(f"[INFO] drone connected, battery: {drone.get_battery()}%")
    drone.streamon()

    drone.takeoff()

    #in case we need to throttle the processing
    frame_counter = 0
    process_every_n_frames = 5

    #main loop
    while True:
        frame = drone.get_frame_read().frame
        frame_counter += 1

        # throttle in case of overloading
        # if frame_counter % process_every_n_frames == 0:

        # detect appropriate object, draw rectangles and get the center to follow
        frame, mask, object_center, object_area, hsv_frame = detect_and_mark_red(frame)

        # adjust the drone position
        adjust_drone_position(drone, frame, object_center, object_area)

        # Show frame
        cv2.imshow("Tracker output", frame)
        cv2.imshow("mask", mask)
        
        cv2.waitKey(1)

main()