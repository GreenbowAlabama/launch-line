# Use a minimal Python base image
FROM --platform=linux/amd64 python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements for better cache utilization
COPY requirements.txt .

# Install system-level dependencies first
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port Flask will listen on
EXPOSE 80

# Run the app
CMD ["python", "app.py"]
