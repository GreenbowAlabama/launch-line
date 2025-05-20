#!/bin/bash

echo "Stopping Flask authentication API..."

if [ -f .flask_auth_pid ]; then
  PID=$(cat .flask_auth_pid)
  echo "Killing process $PID..."
  kill -9 $PID && rm .flask_auth_pid
  echo "Flask authentication server stopped."
else
  echo "No PID file found. Nothing to stop."
fi