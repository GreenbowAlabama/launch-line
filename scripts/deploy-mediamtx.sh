#!/bin/bash

# Usage: ./deploy-mediamtx.sh [env]
# Example: ./deploy-mediamtx.sh dev

set -e

ENV=$1
if [[ -z "$ENV" ]]; then
  echo "Usage: $0 [env]"
  exit 1
fi

RESOURCE_GROUP=${RESOURCE_GROUP:-launch-labs-${ENV}-rg}
K8S_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/k8s"

echo "Deploying MediaMTX from $K8S_DIR/mediamtx.yaml..."

kubectl apply -f "$K8S_DIR/mediamtx.yaml"

echo "Waiting for MediaMTX service to get an external IP..."
sleep 5
for i in {1..20}; do
  EXTERNAL_IP=$(kubectl get svc mediamtx-service -n mediamtx -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || true)
  if [[ -n "$EXTERNAL_IP" ]]; then
    break
  fi
  echo "Waiting for external IP... ($i/20)"
  sleep 5
done

if [[ -z "$EXTERNAL_IP" ]]; then
  echo "Failed to get external IP. Check service status manually:"
  kubectl get svc -n mediamtx
  exit 1
fi

echo "MediaMTX deployed successfully"
echo "Web UI:        http://$EXTERNAL_IP:8888/"
echo "RTMP endpoint: rtmp://$EXTERNAL_IP/live/stream"
echo "RTSP endpoint: rtsp://$EXTERNAL_IP/stream"
