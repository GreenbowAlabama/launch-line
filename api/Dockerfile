# Use a minimal Python base image
FROM python:3.11-slim

# Install required system dependencies for Flask + security deps
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy API source code
COPY . .

# Expose Flask API port
EXPOSE 5050

# Run the Flask server
CMD ["python", "server.py"]