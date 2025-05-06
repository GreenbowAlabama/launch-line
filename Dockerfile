# Use minimal Python image with support for numpy, OpenCV, Torch
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV and other libs
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and YOLO assets
COPY . .

# Expose web server port
EXPOSE 80

# Run Flask app which launches the YOLO script
CMD ["python", "app.py"]
