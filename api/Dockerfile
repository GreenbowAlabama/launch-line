# Use a minimal Python base image
FROM python:3.11-slim

# Install required system dependencies for OpenCV and other dependencies
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

# Add working directory to Python path
ENV PYTHONPATH=/app

# Copy only requirements first (for layer caching)
COPY api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API source code and remaining project files
COPY api/ ./api/
COPY . .

# Expose the Flask API port
EXPOSE 5050

# Start the Flask app
CMD ["python", "api/server.py"]