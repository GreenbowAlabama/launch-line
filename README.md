## `README.md`

```markdown
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
- ✅ Virtual environment setup and clean dependency management

---

## 🧱 Tech Stack

- Python 3.9+
- OpenCV
- YOLOv8 via [Ultralytics](https://github.com/ultralytics/ultralytics)
- macOS or Windows/Linux

---

## 🔧 Setup Instructions

### 1. Clone and set up virtual environment

```bash
git clone https://github.com/GreenbowAlabama/launch-line.git
cd launch-line

python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> Or manually:
```bash
pip install ultralytics opencv-python
```

---

## 📦 Usage

```bash
source .venv/bin/activate  # Activate virtual env
python yolo_main.py        # Run the launch monitor
```

> Press `Q` to exit the app

---

## 📏 Default Setup

- Known distance between cones: `6 feet` (1.8288 meters)
- Camera should be mounted **perpendicular** to ball path
- Detection zone is from Cone A to Cone B

---

## 📸 Camera Tips

- Use 30fps or higher camera
- Mount 4–6 feet from the ball path
- Ensure even lighting across the floor

---

## 📄 License

MIT License

---

## 🤝 Contributing

Pull requests and issues welcome!  
Got cool use cases, garage setups, or speed records? Submit them!
```

---

## ✅ `.gitignore`

Create a `.gitignore` file in your project root with:

```gitignore
# Python virtual environment
.venv/
__pycache__/
*.pyc

# Mac system files
.DS_Store

# VS Code settings (optional)
.vscode/

# OS trash / metadata
.Trashes
ehthumbs.db
Thumbs.db
Icon?

# Logs
*.log

# Env-specific files
.env
```

---

## ✅ Final Touch: Freeze Your Environment

If not already done:

```bash
pip freeze > requirements.txt
```