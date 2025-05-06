#!/bin/bash
set -e

# === Inputs ===
ENV=$1
RESOURCE_GROUP="launch-labs-${ENV}-rg"
AKS_NAME="launch-labs-aks"

echo "Node pool status for cluster [$AKS_NAME] in [$ENV]:"

az aks nodepool list \
  --resource-group $RESOURCE_GROUP \
  --cluster-name $AKS_NAME \
  --output table \
  --query "[].{Name:name, VMSize:vmSize, Count:count, Mode:mode, Status:powerState.code}"
