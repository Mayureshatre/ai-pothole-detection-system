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
