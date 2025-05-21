# api/Dockerfile
FROM python:3.11-slim

# System dependencies for bcrypt (used by passlib)
RUN apt-get update && apt-get install -y build-essential libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Set working dir
WORKDIR /app

# Install Python dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy API source code
COPY . .

EXPOSE 5050

CMD ["python", "server.py"]