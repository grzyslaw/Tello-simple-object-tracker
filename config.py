TUNING_PARAMS = {
    #divisors for offsets to make movements more smooth
    'yaw_scale': 10, 
    'ud_scale': 8,
    'fb_scale': 2000,
    #tello's rc_control operates on range <-100;100>, but they are clipped to achive more smooth movements
    'yaw_clip': 90,
    'ud_clip': 60,
    'fb_clip': 30,
    #deadzones to prevent overcorrection, and to much unnecesary movements
    'deadzone_x': 30,
    'deadzone_y': 30,
    'deadzone_area': 3000,
    #detected object area / frame area, used for proximity
    'target_ratio': 0.20,
    #cap for drone flight height 
    'max_height': 190,
    'move_duration': 0.05
}