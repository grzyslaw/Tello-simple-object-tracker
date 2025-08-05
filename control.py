from djitellopy import Tello
import cv2
import numpy as np
import time

MAX_HEIGHT = 190 #cm

def move_delta(drone: Tello, lr=0, fb=0, ud=0, yaw=0, duration=0.05):
    #send move command
    drone.send_rc_control(lr,fb,ud,yaw)
    #wait some time to execute the movement
    time.sleep(duration)
    #send stop command
    drone.send_rc_control(0,0,0,0)

def adjust_drone_position(drone: Tello, frame, object_center, object_area):
    #when there is no object in frame, return
    if object_center == (-1,-1): return

    #get the frame center and draw a circle to mark it
    frame_h, frame_w = frame.shape[:2]
    cv2.circle(frame, (frame_w // 2, frame_h // 2), 3, (0, 255, 0), 2)

    #calculate position offset
    offsets = np.array([0,0,0]) #x-offset (left right), y-offset (up down), z-offset (proximity)
    offsets[0] = object_center[0] - frame_w // 2 #x
    offsets[1] = object_center[1] - frame_h // 2 #y
    #z
    frame_area = frame_h * frame_w
    target_ratio = 0.20 #percent of frame area covered
    target_object_area = frame_area * target_ratio
    offsets[2] = object_area - target_object_area 

    #tello's rc_control operates on range <-100;100>, and camera operates on 720x920 px, hence will be deviding the offset 
    #to smoothen the movements, also might tighten the range with a clip after some irl experiments
    yaw = int(np.clip(offsets[0] / 10, -90, 90))
    ud = int(np.clip(-offsets[1] / 8, -60, 60))
    fb = int(np.clip(-offsets[2] / 2000, -30, 30))

    #dead zones, again for smoothing
    if abs(offsets[0]) < 30: yaw = 0
    if abs(offsets[1]) < 30: ud = 0
    if abs(offsets[2]) < 3000: fb = 0

    current_height = drone.get_height()
    if current_height >= MAX_HEIGHT and ud > 0:
        print("ceilling reached - blocking upward movement")
        ud = 0

    print(f"moving: yaw: {yaw}, ud: {ud}, fb: {fb}")
    move_delta(drone, fb=fb, ud=ud, yaw=yaw)

