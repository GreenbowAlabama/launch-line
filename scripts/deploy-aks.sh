#!/bin/bash
set -e

# === Inputs ===
ENV=$1
LOCATION="eastus"
RESOURCE_GROUP="launch-labs-${ENV}-rg"
AKS_NAME="launch-labs-aks"
STANDARD_POOL="standardpool"
GPU_POOL="gpupool"
ENABLE_GPU=false

if [[ "$2" == "--scale-gpu" ]]; then
  ENABLE_GPU=true
fi

echo "Using resource group: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location $LOCATION

if ! az aks show --resource-group $RESOURCE_GROUP --name $AKS_NAME &>/dev/null; then
  echo "Creating AKS cluster..."
  az aks create \
    --resource-group $RESOURCE_GROUP \
    --name $AKS_NAME \
    --location $LOCATION \
    --enable-managed-identity \
    --nodepool-name $STANDARD_POOL \
    --node-vm-size Standard_B2s \
    --node-count 1 \
    --enable-addons monitoring \
    --generate-ssh-keys
else
  echo "AKS cluster already exists, skipping create."
fi

if ! az aks nodepool show --cluster-name $AKS_NAME --resource-group $RESOURCE_GROUP --name $GPU_POOL &>/dev/null; then
  echo "Creating GPU node pool..."
  az aks nodepool add \
    --resource-group $RESOURCE_GROUP \
    --cluster-name $AKS_NAME \
    --name $GPU_POOL \
    --node-count 0 \
    --node-vm-size Standard_NC4as_T4_v3 \
    --node-taints sku=gpu:NoSchedule \
    --labels sku=gpu \
    --mode User
else
  echo "GPU node pool already exists."
fi

if [ "$ENABLE_GPU" = true ]; then
  echo "Scaling GPU node pool to 1..."
  az aks nodepool scale \
    --resource-group $RESOURCE_GROUP \
    --cluster-name $AKS_NAME \
    --name $GPU_POOL \
    --node-count 1
else
  echo "GPU pool remains scaled to 0."
fi

az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_NAME --overwrite-existing
echo "AKS cluster setup complete."
