from djitellopy import Tello
import cv2
import numpy as np
import time

class DroneController:
    def __init__(self, drone: Tello, max_height=190,
                 yaw_scale=10, ud_scale=8, fb_scale=2000,
                 yaw_clip=90, ud_clip=30, fb_clip=30,
                 deadzone_x=30, deadzone_y=30, deadzone_area=3000,
                 target_ratio=0.20, move_duration=0.05):
        
        self.drone = drone
        self.max_height = max_height

        self.yaw_scale = yaw_scale
        self.ud_scale = ud_scale
        self.fb_scale = fb_scale

        self.yaw_clip = yaw_clip
        self.ud_clip = ud_clip
        self.fb_clip = fb_clip

        self.deadzone_x = deadzone_x
        self.deadzone_y = deadzone_y
        self.deadzone_area = deadzone_area

        self.target_ratio = target_ratio
        
        self.move_duration = move_duration

    def move_delta(self, lr=0, fb=0, ud=0, yaw=0, move_duration=0.05):
        #send move command
        self.drone.send_rc_control(lr,fb,ud,yaw)
        #wait some time to execute the movement
        time.sleep(move_duration)
        #send stop command
        self.drone.send_rc_control(0,0,0,0)

    def adjust_position(self, frame, object_center, object_area):
        #when there is no object in frame, return
        if object_center == (-1,-1): return

        #get the frame center and draw a circle to mark it
        frame_h, frame_w = frame.shape[:2]
        cv2.circle(frame, (frame_w // 2, frame_h // 2), 3, (0, 255, 0), 2)

        #calculate position offset
        offsets = np.array([
            object_center[0] - frame_w // 2, #horizontal
            object_center[1] - frame_h // 2, #vertical
            object_area - (frame_h * frame_w * self.target_ratio) #proximity 
        ])

        #tello's rc_control operates on range <-100;100>, and camera operates on 720x920 px, hence will be deviding the offset 
        #to smoothen the movements, also using clips for better results
        yaw = int(np.clip(offsets[0] / self.yaw_scale, -self.yaw_clip, self.yaw_clip))
        ud  = int(np.clip(-offsets[1] / self.ud_scale, -self.ud_clip, self.ud_clip))
        fb  = int(np.clip(-offsets[2] / self.fb_scale, -self.fb_clip, self.fb_clip))

        #deadzones
        if abs(offsets[0]) < self.deadzone_x: yaw = 0
        if abs(offsets[1]) < self.deadzone_y: ud = 0
        if abs(offsets[2]) < self.deadzone_area: fb = 0

        height = self.drone.get_height()
        if height >= self.max_height and ud > 0:
            print("Ceiling reached - blocking upward movement")
            ud = 0

        print(f"Moving: yaw={yaw}, ud={ud}, fb={fb}")
        self.move_delta(fb=fb, ud=ud, yaw=yaw, move_duration=self.move_duration)