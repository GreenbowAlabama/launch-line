# syntax=docker/dockerfile:1.4

### Step 1: Build UI
FROM node:18-alpine AS ui-builder
WORKDIR /app/ui
COPY ui/package*.json ./
RUN npm ci
COPY ui/ .
RUN npm run build

### Step 2: Build Python API
FROM python:3.11-slim AS api-builder
WORKDIR /app

# Install system packages for OpenCV and Flask
RUN apt-get update && apt-get install -y \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 ffmpeg \
    nginx supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy API code
COPY api/ ./api

# Copy built UI into NGINX web root
COPY --from=ui-builder /app/ui/dist /usr/share/nginx/html

# Copy NGINX and supervisord configs
COPY deploy/nginx.conf /etc/nginx/nginx.conf
COPY deploy/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports
EXPOSE 80 5050

# Start both services
CMD ["/usr/bin/supervisord"]