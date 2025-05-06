#!/bin/bash
set -e

ENV=$1
RESOURCE_GROUP="launch-labs-${ENV}-rg"
AKS_NAME="launch-labs-aks"

echo "Scaling GPU pool to 0..."
az aks nodepool scale \
  --resource-group "$RESOURCE_GROUP" \
  --cluster-name "$AKS_NAME" \
  --name gpu \
  --node-count 0 \
  --no-wait

echo "Optionally scale app down (uncomment if needed)..."
# kubectl scale deployment launch-labs-app --replicas=0
# kubectl scale deployment mediamtx -n mediamtx --replicas=0
