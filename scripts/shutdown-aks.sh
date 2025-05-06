#!/bin/bash
set -e

# === Inputs ===
ENV=$1
RESOURCE_GROUP="launch-labs-${ENV}-rg"
AKS_NAME="launch-labs-aks"

echo "Shutting down AKS cluster node pools for ENV: $ENV..."

NODEPOOLS=$(az aks nodepool list \
  --resource-group $RESOURCE_GROUP \
  --cluster-name $AKS_NAME \
  --query "[?mode=='User'].name" -o tsv)

if [ -z "$NODEPOOLS" ]; then
  echo "No User-mode node pools found to scale down."
  exit 0
fi

for POOL in $NODEPOOLS; do
  echo "Scaling user pool '$POOL' to 0..."
  az aks nodepool scale \
    --resource-group $RESOURCE_GROUP \
    --cluster-name $AKS_NAME \
    --name "$POOL" \
    --node-count 0
done

echo "All user node pools scaled to 0. System pools remain active."
