#!/bin/bash
set -e

ENV=$1
RESOURCE_GROUP="launch-labs-${ENV}-rg"
AKS_NAME="launch-labs-aks"
POOL_NAME="gpu"

echo "Checking current node count for GPU pool in $ENV..."

CURRENT_COUNT=$(az aks nodepool show \
  --resource-group "$RESOURCE_GROUP" \
  --cluster-name "$AKS_NAME" \
  --name "$POOL_NAME" \
  --query "count" -o tsv)

if [[ "$CURRENT_COUNT" -ge 1 ]]; then
  echo "GPU pool is already scaled to $CURRENT_COUNT node(s). Skipping scale-up."
  exit 0
fi

echo "Scaling GPU pool to 1..."
az aks nodepool scale \
  --resource-group "$RESOURCE_GROUP" \
  --cluster-name "$AKS_NAME" \
  --name "$POOL_NAME" \
  --node-count 1 \
  --no-wait
