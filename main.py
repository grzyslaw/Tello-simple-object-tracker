from djitellopy import Tello
import cv2
from color_tracker import detect_and_mark_red
from drone_controller import DroneController

from config import TUNING_PARAMS

# function to debug color manualy
# example usage cv2.setMouseCallback("Tracker output", show_hsv_values, hsv_frame)
def show_hsv_values(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        hsv_val = param[y, x]  # row = y, column = x
        print(f"HSV @ ({x},{y}): {hsv_val}")

def main(should_fly:bool, use_tuning_params:bool): 
    #initialize tello
    drone = Tello()

    #connect tello and start stream
    drone.connect()
    print(f"[INFO] drone connected, battery: {drone.get_battery()}%")
    drone.streamon()

    if should_fly: drone.takeoff()

    #controller initialization
    controller = None
    if use_tuning_params: controller = DroneController(drone, **TUNING_PARAMS)
    else: controller = DroneController(drone)

    #main loop
    while True:
        frame = drone.get_frame_read().frame

        # detect appropriate object, draw rectangles and get the center to follow
        frame, mask, object_center, object_area, hsv_frame = detect_and_mark_red(frame)

        # adjust the drone position
        controller.adjust_position(frame, object_center, object_area)

        # Show frame
        cv2.imshow("Tracker output", frame)
        cv2.waitKey(1)

main(True,False)