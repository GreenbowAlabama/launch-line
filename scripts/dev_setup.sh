#!/bin/bash
set -e

# Step 1: Set up Python virtual environment
if [ ! -d ".venv" ]; then
  echo "[INFO] Creating virtual environment..."
  python3 -m venv .venv
fi

source .venv/bin/activate
echo "[INFO] Virtual environment activated."

# Step 2: Install dependencies
echo "[INFO] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Set environment variables
echo "[INFO] Setting local environment variables..."
export MEDIA_SERVER="http://localhost:8888"
export RTSP_STREAM_URL="rtsp://localhost:8554/live/stream"

# Optional Step 4: Start MediaMTX container (if not already running)
if ! docker ps | grep -q mediamtx-dev; then
  echo "[INFO] Starting MediaMTX via Docker..."
  docker run -d \
    --name mediamtx-dev \
    -p 8554:8554 -p 1935:1935 -p 8888:8888 \
    bluenviron/mediamtx
else
  echo "[INFO] MediaMTX already running."
fi

echo "[✅] Setup complete. You can now run the app with: python app.py"