# Real-Time AI Pothole Detection System 🛣️🤖

A real-time computer vision desktop application built with **YOLOv8**, **OpenCV**, and **Tkinter** to detect, count, and track road potholes from video files or live camera feeds.

This project is optimized for deployment on resource-constrained environments like a **Raspberry Pi** using direct-connectivity VNC mobile streaming, or as a vehicle dashboard-mounted edge application.

---

## ✨ Features

- **High-Accuracy Object Detection:** Utilizing a custom-trained **YOLOv8** model (`best.pt`) optimized for low-latency inference on road distress anomalies.
- **Flicker-Free Thread-Decoupled GUI:** Engineered a stable **Tkinter** GUI using a dedicated background worker thread for AI processing. Frame rendering is managed safely via an asynchronous loop, completely preventing window stutter or flicker.
- **Smart Bounding-Box Geometry Filtering:** Implemented an automated aspect-ratio filter ($h/w$) to eliminate false-positive vertical structures (e.g., pedestrians, poles, trees) common in standalone custom detection datasets.
- **Multi-Input Support:** Seamlessly toggle between localized video file testing (`.mp4`, `.avi`, `.mov`) and real-time webcam/USB camera streaming.

---

## 🛠️ Architecture & Tech Stack

- **Language:** Python 3.8+
- **Deep Learning Model:** YOLOv8 (Ultralytics)
- **Computer Vision Processing:** OpenCV-Python
- **Graphical User Interface:** Tkinter
- **Multithreading:** Python `threading` library (Daemon Threads)
- **Image Conversion:** Pillow (PIL)

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python installed on your system. It is highly recommended to set up a virtual environment.

```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/ai-pothole-detection-system.git](https://github.com/YOUR_USERNAME/ai-pothole-detection-system.git)
cd ai-pothole-detection-system
```

### 2. Install Dependencies:

Install the required packages using pip:

```bash
pip install ultralytics opencv-python pillow
```

### 3. Place Model Weights

Make sure your custom-trained YOLO weights file is named best.pt and placed in the root directory of this project folder.

### 4. Run the Application

```bash
python main.py
```

## 📱 Embedded & Raspberry Pi Deployment

This application is fully feasible for compact hardware setups like a Raspberry Pi 4 / 5:

1. Hardware Option: Use a 5-inch/7-inch touch display directly connected via HDMI/DSI.

2. Headless Mobile Stream (VNC): \* Enable the built-in VNC server on your Raspberry Pi via sudo raspi-config (Interface Options -> VNC -> Enable).

   Host a local Wi-Fi hotspot from your mobile device and connect the Pi to it.

   Open RealVNC Viewer (or any free alternative client) on your smartphone, input the Pi's local IP address (hostname -I), and interact with the application GUI wirelessly directly from your phone screen.

## 🔍 Code Implementation Highlights

### Anti-Flicker GUI Buffer Loop

Instead of updating the GUI inside the intensive video parsing frame loop, frames are passed to a safe storage pointer and drawn via standard tick scheduling, decoupling computation from rendering:

```python
def update_gui_loop(self):
    if self.latest_imgtk:
        self.video_label.imgtk = self.latest_imgtk
        self.video_label.configure(image=self.latest_imgtk)
    self.root.after(30, self.update_gui_loop)
```

### Geometric Domain-Shift Mitigation (Aspect-Ratio Filter)

Prevents false-positive vehicle dashboard encounters with humans or street signs by evaluating bounding box dimensions:

```python
# If the bounding box is taller than it is wide, drop the prediction
aspect_ratio = height / width
if aspect_ratio > 1.2:
    continue # Skips rendering/counting non-flat anomalies
```
