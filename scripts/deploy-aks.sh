#!/bin/bash

# === Inputs ===
ENV=$1
LOCATION="eastus"
RESOURCE_GROUP="launch-labs-${ENV}-rg"
AKS_NAME="launch-labs-aks"

# === Check input ===
if [ -z "$ENV" ]; then
  echo "Usage: ./scripts/deploy-aks.sh <environment>"
  exit 1
fi

# === Create Resource Group (if not exists) ===
echo "Ensuring resource group: $RESOURCE_GROUP exists..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

# === Check if AKS cluster already exists ===
if az aks show --resource-group "$RESOURCE_GROUP" --name "$AKS_NAME" > /dev/null 2>&1; then
  echo "AKS cluster $AKS_NAME already exists, skipping creation."
else
  echo "Creating AKS cluster: $AKS_NAME..."
  az aks create \
    --resource-group $RESOURCE_GROUP \
    --name launch-labs-aks \
    --node-count 1 \
    --enable-managed-identity \
    --enable-addons monitoring \
    --node-vm-size Standard_A2_v2 \
    --generate-ssh-keys
fi

# === Add GPU Node Pool (if not exists) ===
if az aks nodepool show --resource-group "$RESOURCE_GROUP" --cluster-name "$AKS_NAME" --name gpu > /dev/null 2>&1; then
  echo "GPU node pool already exists, skipping addition."
else
  echo "Adding GPU node pool to $AKS_NAME..."
  az aks nodepool add \
    --resource-group $RESOURCE_GROUP \
    --cluster-name launch-labs-aks \
    --name gpu \
    --node-count 1 \
    --node-vm-size standard_d2s_v3 \
    --labels workload=gpu \
    --mode User \
    --node-taints sku=gpu:NoSchedule
fi

echo "✅ AKS cluster $AKS_NAME with GPU support is ready in '$ENV' environment."
