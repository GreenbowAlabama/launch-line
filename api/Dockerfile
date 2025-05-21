# Use a minimal Python base image
FROM python:3.11-slim

# Install required system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements first for caching
COPY api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire API source code into the container
COPY api/ ./api/

# Expose the Flask API port
EXPOSE 5050

# Run the Flask server
CMD ["python", "api/server.py"]