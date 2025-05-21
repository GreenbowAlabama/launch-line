# Use a minimal Python base image
FROM python:3.11-slim

# Install system dependencies required for OpenCV and media processing
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

# Copy requirements file from the API folder
COPY api/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire API source code into the container
COPY api/ ./api/

# Expose the Flask API port
EXPOSE 5050

# Set the default command to run the Flask API (assuming entry point is api/server.py)
CMD ["python", "api/server.py"]