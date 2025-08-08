from djitellopy import Tello
import cv2
from color_tracker import detect_and_mark_red
from drone_controller import DroneController
from flight_monitor import FlightMonitor

from config import TUNING_PARAMS

# function to debug color manualy
# example usage cv2.setMouseCallback("Tracker output", show_hsv_values, hsv_frame)
def show_hsv_values(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        hsv_val = param[y, x]  # row = y, column = x
        print(f"HSV @ ({x},{y}): {hsv_val}")

def main(should_fly:bool, setup_name): 
    #initialize tello
    drone = Tello()

    #connect tello and start stream
    drone.connect()
    print(f"[INFO] drone connected, battery: {drone.get_battery()}%")
    drone.streamon()

    if should_fly: drone.takeoff()

    #monitor initialization
    monitor = FlightMonitor(setup_name)
    print("[INFO] flight monitor initialized")

    #controller initialization
    controller = DroneController(drone, monitor, **TUNING_PARAMS)
    print("[INFO] flight controller initialized")

    #main loop
    try:
        while True:
            frame = drone.get_frame_read().frame

            # detect appropriate object, draw rectangles and get the center to follow
            frame, mask, object_center, object_area, hsv_frame = detect_and_mark_red(frame)

            # adjust the drone position
            controller.adjust_position(frame, object_center, object_area)

            # Show frame
            cv2.imshow("Tracker output", frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                print("[INFO] 'q' pressed - exiting loop")
                break

    except KeyboardInterrupt:
        print("[WARN] KeyboardInterupt - exiting...")

    finally:
        #land if flying
        if should_fly:
            print("[INFO] landing...")
            drone.land()

        #stop stream and kill OpenCV windows
        drone.streamoff()
        cv2.destroyAllWindows()

        #save and plot the flight data
        print("[INFO] generating plots...")
        monitor.plot_flight_data()

        print("[INFO] Done, all good, signing off...")

main(True,"test_monitor_3")