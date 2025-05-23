#!/bin/bash
set -e

ENV=$1
RESOURCE_GROUP="launch-labs-${ENV}-rg"
AKS_NAME="launch-labs-aks"

echo "Scaling GPU pool to 0 in $ENV..."

az aks nodepool scale \
  --resource-group "$RESOURCE_GROUP" \
  --cluster-name "$AKS_NAME" \
  --name gpu \
  --node-count 0 \
  --no-wait
