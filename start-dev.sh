#!/bin/bash

echo "Starting Flask authentication API..."

# Activate virtual environment
if [ -d ".venv311" ]; then
  echo "Activating virtualenv (.venv311)..."
  source .venv311/bin/activate
else
  echo "Missing virtualenv (.venv311). Run python3 -m venv .venv311 first."
  exit 1
fi

# Kill any process using port 5050
PORT_PID=$(lsof -ti tcp:5050)
if [ ! -z "$PORT_PID" ]; then
  echo "Port 5050 in use by process $PORT_PID. Killing it..."
  kill -9 $PORT_PID
  sleep 1
fi

# Start Flask app using PYTHONPATH
echo "Starting Flask auth service on port 5050..."
PYTHONPATH=. nohup python3 api/server.py > auth-flask.log 2>&1 &

echo "Waiting for Flask to start on http://localhost:5050 ..."

# Wait for the /health endpoint to be ready
RETRIES=15
for i in $(seq 1 $RETRIES); do
  if curl --output /dev/null --silent --head --fail http://localhost:5050/health; then
    echo "Flask API is up!"
    exit 0
  else
    sleep 1
  fi
done

echo "Failed to detect Flask on port 5050 after $RETRIES seconds."
echo "Check logs: tail -f auth-flask.log"
exit 1