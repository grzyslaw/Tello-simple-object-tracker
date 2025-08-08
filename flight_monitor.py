import csv
import json
import os
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from config import TUNING_PARAMS

HEADER = ["timestamp", "offset_x", "offset_y", "offset_area", "yaw", "ud", "fb", "height", "object_detected"]

class FlightMonitor:
    def __init__(self,setup_name):
        timestamp = datetime.datetime.now().isoformat().replace(":","-")

        directory_name = str(setup_name) + "_" + timestamp
        self.dir_name = os.path.join("flights",directory_name)
        
        #create directory for data
        os.mkdir(self.dir_name)
        
        #save params as json
        with open(os.path.join(self.dir_name, "params.json"), "w") as f: 
            json.dump(TUNING_PARAMS, f, indent=4)

        #create csv file for flight data
        with open(os.path.join(self.dir_name, "flight_data.csv"), "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(HEADER)

    
    def save_flight_data(self, offset_x, offset_y, 
                         offset_area, yaw, 
                         ud, fb, height, 
                         object_detected
                        ):
        with open(os.path.join(self.dir_name, "flight_data.csv"), "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.datetime.now().isoformat(), offset_x, offset_y, 
                offset_area, yaw, ud, fb, height, object_detected
                ])
            
    def plot_flight_data(self):
        #load csv
        df = pd.read_csv(os.path.join(self.dir_name, "flight_data.csv"))

        #parse timestamp as datetime
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        #plot 1: Offset X vs Yaw
        plt.figure()
        plt.scatter(df["offset_x"], df["yaw"], alpha=0.5)
        plt.xlabel("Offset X (px)")
        plt.ylabel("Yaw")
        plt.title("Offset X vs Yaw")
        plt.grid(True)
        plt.savefig(os.path.join(self.dir_name, "offset_x_vs_yaw.png"))
        plt.close()

        #plot 2: Offset Y vs Up/Down (UD)
        plt.figure()
        plt.scatter(df["offset_y"], df["ud"], alpha=0.5)
        plt.xlabel("Offset Y (px)")
        plt.ylabel("Up/Down")
        plt.title("Offset Y vs UD")
        plt.grid(True)
        plt.savefig(os.path.join(self.dir_name, "offset_y_vs_ud.png"))
        plt.close()

        #plot 3: Offset Area vs Forward/Backward (FB)
        plt.figure()
        plt.scatter(df["offset_area"], df["fb"], alpha=0.5)
        plt.xlabel("Offset Area")
        plt.ylabel("Forward/Backward")
        plt.title("Offset Area vs FB")
        plt.grid(True)
        plt.savefig(os.path.join(self.dir_name, "offset_area_vs_fb.png"))
        plt.close()

        #plot 4: Height over Time
        plt.figure()
        plt.plot(df["timestamp"], df["height"])
        plt.xlabel("Time")
        plt.ylabel("Height (cm)")
        plt.title("Drone Height Over Time")
        plt.grid(True)
        plt.savefig(os.path.join(self.dir_name, "height_over_time.png"))
        plt.close()

        #plot 5: Object Detection Timeline
        plt.figure()
        df["object_detected"] = df["object_detected"].astype(int)
        plt.plot(df["timestamp"], df["object_detected"])
        plt.xlabel("Time")
        plt.ylabel("Object Detected (1=yes, 0=no)")
        plt.title("Object Detection Timeline")
        plt.grid(True)
        plt.savefig(os.path.join(self.dir_name, "object_detection_timeline.png"))
        plt.close()
                 