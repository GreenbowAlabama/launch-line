#!/bin/bash
set -e

echo "[INFO] Tearing down development environment..."

# Step 1: Stop MediaMTX container if running
if docker ps | grep -q mediamtx-dev; then
  echo "[INFO] Stopping MediaMTX container..."
  docker stop mediamtx-dev >/dev/null
  docker rm mediamtx-dev >/dev/null
else
  echo "[INFO] MediaMTX container not running."
fi

# Step 2: Deactivate virtualenv if active
if [[ "$VIRTUAL_ENV" != "" ]]; then
  echo "[INFO] Deactivating virtual environment..."
  deactivate || true
fi

# Step 3: Optionally clean .venv directory
if [[ "$1" == "--clean" ]]; then
  echo "[INFO] Removing .venv..."
  rm -rf .venv
fi

echo "[✅] Teardown complete."