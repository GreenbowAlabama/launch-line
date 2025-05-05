# Use a minimal Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install dependencies without caching wheels
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port your app listens on (change if needed)
EXPOSE 80

# Run your app (change to match your actual entry point)
CMD ["python", "app.py"]
