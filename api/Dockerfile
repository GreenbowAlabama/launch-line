# api/Dockerfile
FROM python:3.11-slim

# Install required system dependencies
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

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy API source code
COPY api/ ./api/
COPY server.py .

# Expose the Flask API port
EXPOSE 5050

# Start the API
CMD ["python", "server.py"]
