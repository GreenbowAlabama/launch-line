# Use a minimal Python base image
FROM python:3.11-slim

# Install system dependencies needed for some Python packages (if any)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full application code
COPY . .

# Expose the Flask API port
EXPOSE 5050

# Run the Flask app
CMD ["python", "api/server.py"]