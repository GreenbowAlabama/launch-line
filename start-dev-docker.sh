#!/bin/bash
set -e

echo "Starting local MediaMTX container using Docker Compose..."

# Create config directory if missing
mkdir -p config

# Ensure a config file exists
if [[ ! -f config/mediamtx.yml ]]; then
  echo "Missing config/mediamtx.yml. Please provide your MediaMTX config file before running."
  exit 1
fi

# Launch MediaMTX container
docker-compose up -d

# Display container IP for Larix configuration
CONTAINER_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mediamtx)
echo "MediaMTX is running at:"
echo "  RTMP: rtmp://$CONTAINER_IP/live/stream"
echo "  HLS UI: http://$CONTAINER_IP:8888/"
echo "  API: http://$CONTAINER_IP:9997/"

# Optional: auto-launch the Flask app with your original start-dev.sh
if [[ -f start-dev.sh ]]; then
  echo "Launching app using start-dev.sh..."
  ./start-dev.sh
fi