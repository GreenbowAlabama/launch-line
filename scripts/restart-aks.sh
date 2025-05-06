#!/bin/bash
set -e

# === Inputs ===
ENV=$1
RESOURCE_GROUP="launch-labs-${ENV}-rg"
AKS_NAME="launch-labs-aks"
STANDARD_POOL="standardpool"
GPU_POOL="gpupool"

# Desired node counts
STANDARD_COUNT=1
GPU_COUNT=1

echo "Restarting node pools for ENV: $ENV..."

echo "Scaling $STANDARD_POOL to $STANDARD_COUNT..."
az aks nodepool scale \
  --resource-group $RESOURCE_GROUP \
  --cluster-name $AKS_NAME \
  --name $STANDARD_POOL \
  --node-count $STANDARD_COUNT

echo "Scaling $GPU_POOL to $GPU_COUNT..."
az aks nodepool scale \
  --resource-group $RESOURCE_GROUP \
  --cluster-name $AKS_NAME \
  --name $GPU_POOL \
  --node-count $GPU_COUNT

echo "Node pools restarted."
