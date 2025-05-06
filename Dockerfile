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

# Install dependencies without caching wheels
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code and assets
COPY . .

COPY soccer_field.jpg .

# Expose the port your app listens on
EXPOSE 80

# Run your app
CMD ["python", "app.py"]
