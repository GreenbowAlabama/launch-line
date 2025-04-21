# Launch Line ⚽📸  
_A DIY Soccer Ball Speed Tracker using YOLOv8 and Computer Vision_

![Demo Screenshot](assets/demo.gif)

---

## 🚀 Overview

**Launch Line** is a real-time launch monitor for soccer players, coaches, and enthusiasts. It uses an external or wireless camera, YOLOv8 object detection, and motion tracking to measure ball speed based on its movement through a known distance (e.g., 6 feet).

---

## 🎯 Features

- ✅ Live video feed with object detection (YOLOv8)
- ✅ Automatic ball tracking using bounding boxes
- ✅ Speed calculation in mph, ft/s, and m/s
- ✅ Support for Continuity Camera (iPhone) or USB webcams
- ✅ Easy to configure and extend for other sports

---

## 🧱 Tech Stack

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- OpenCV
- Python 3.9+
- macOS or Windows/Linux

---

## 🔧 Installation

```bash
git clone https://github.com/yourname/launch-line.git
cd launch-line
pip install -r requirements.txt
