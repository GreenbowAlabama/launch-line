# Use a minimal Python base image
FROM --platform=linux/amd64 python:3.11-slim

# Install required system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project contents into the image
COPY . .

# Expose both Flask API (5050) and optional frontend (5173) if ever needed
EXPOSE 5050
EXPOSE 5173

# Set the default command to run the Flask API
CMD ["python", "api/server.py"]