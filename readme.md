# DJI Tello Simple Object Tracker

A Python-based **object tracking and control system** for the DJI Tello drone, featuring live video tracking, tunable flight parameters, and automatic logging of flight statistics with visualization.

## ✨ Features

- **Real-time object tracking** based on color detection (default: blue objects).
- **Automatic drone control** to follow the tracked object using yaw, forward/backward, and up/down adjustments.
- **Tunable parameters** for fine-grained control of drone behavior.
- **Flight logging system**:
  - Saves current tuning parameters as JSON.
  - Records flight data (offsets, control commands, height, etc.) in CSV.
  - Generates plots for post-flight analysis.
- **Safe stop**: Land the drone and generate plots without killing the script (by pressing 'q').

---

## 📂 Project Structure

```
Tello-simple-object-tracker/
│
├── main.py                  # Main entry point
├── drone_controller.py      # Drone control logic
├── color_tracker.py         # Object detection & tracking
├── flight_monitor.py        # Logging and plotting class
├── config.py                # Tuning parameters
├── flights/                 # Saved flight logs and plots
├── requirements.txt         # Dependencies
└── README.md                # This file

```

---

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Tello-simple-object-tracker.git
   cd Tello-simple-object-tracker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

1. **Turn on your DJI Tello** and connect to its Wi-Fi.
2. **Run the script:**
   ```bash
   python main.py
   ```
3. **Controls:**
   - The drone will track the target automatically.
   - Press `q` in the display window to **land and generate plots**.

---

## 📊 Flight Data & Plots

Each flight creates a folder inside `flights/`:
- **`params.json`** → tuning parameters used in this run.
- **`flight_data.csv`** → timestamped log of:
  - Pixel offsets (X, Y) from object center.
  - Offset area (size difference from target).
  - Control commands sent (yaw, forward/backward, up/down).
  - Drone height.
  - Whether an object was detected.
- **Generated plots**:
  1. **Offset X vs Yaw** → Shows how yaw corrections correspond to horizontal offset.
  2. **Offset Y vs UD** → Shows vertical control in relation to vertical offset.
  3. **Offset Area vs FB** → Correlation between object size difference and forward/backward movement.
  4. **Height over Time** → Drone altitude trends.
  5. **Object Detection Timeline** → When the object was detected during the flight.

---

## 🔧 Tuning Guide

- **Dead zones**: Prevents small offsets from triggering movement.  
- **Speed multipliers**: Scales how aggressively the drone responds.  
- **Offset area target**: Helps maintain optimal distance from the object.

You can adjust these in `config.py` and re-run to test.

---

## 📜 License

MIT License — feel free to use, modify, and share.

---

## 🙌 Credits

Built with:
- [DJITelloPy](https://github.com/damiafuentes/DJITelloPy)
- OpenCV
- Pandas
- Matplotlib

---
