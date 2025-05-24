#!/bin/bash
set -e

RESOURCE_GROUP="launch-labs-prod-rg"
CLUSTER_NAME="launch-labs-prod-aks"
IP_NAME="launch-labs-prod-egress-ip"
LOCATION="eastus"

# Create static public IP
echo "Creating static public IP..."
az network public-ip create \\
  --resource-group $RESOURCE_GROUP \\
  --name $IP_NAME \\
  --sku Standard \\
  --allocation-method static \\
  --location $LOCATION

# Get full resource ID of the public IP
echo "Retrieving Public IP Resource ID..."
EGRESS_IP_ID=$(az network public-ip show \\
  --resource-group $RESOURCE_GROUP \\
  --name $IP_NAME \\
  --query "id" -o tsv)

# Assign it to AKS as outbound IP
echo "Updating AKS cluster to use static outbound IP..."
az aks update \\
  --resource-group $RESOURCE_GROUP \\
  --name $CLUSTER_NAME \\
  --load-balancer-outbound-ips "$EGRESS_IP_ID"

echo "Egress IP setup complete."