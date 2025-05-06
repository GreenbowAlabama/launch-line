#!/bin/bash

set -e

ENV=$1
RESOURCE_GROUP=${RESOURCE_GROUP:-launch-labs-${ENV}-rg}
K8S_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)/k8s"

echo "Deploying MediaMTX using $K8S_DIR/mediamtx.yaml..."

# Apply the configuration
kubectl apply -f "$K8S_DIR/mediamtx.yaml"

echo "Waiting for MediaMTX LoadBalancer to get an external IP..."
sleep 5

for i in {1..20}; do
  EXTERNAL_IP=$(kubectl get svc mediamtx -n mediamtx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  if [[ -n "$EXTERNAL_IP" ]]; then
    break
  fi
  echo "Waiting for external IP... ($i/20)"
  sleep 5
done

if [[ -z "$EXTERNAL_IP" ]]; then
  echo "Failed to retrieve external IP. You may need to check the service manually:"
  kubectl get svc -n mediamtx
  exit 1
fi

echo "MediaMTX deployed successfully!"
echo "Stream Management UI:   http://$EXTERNAL_IP:8888/"
echo "RTMP ingest endpoint:   rtmp://$EXTERNAL_IP:1935/live/stream"
