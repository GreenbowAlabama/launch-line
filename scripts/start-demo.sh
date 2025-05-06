#!/bin/bash
set -e

ENV=$1
RESOURCE_GROUP="launch-labs-${ENV}-rg"
AKS_NAME="launch-labs-aks"

echo "Scaling GPU pool to 1..."
az aks nodepool scale \
  --resource-group "$RESOURCE_GROUP" \
  --cluster-name "$AKS_NAME" \
  --name gpu \
  --node-count 1 \
  --no-wait

echo "Waiting 60s for node readiness..."
sleep 60

echo "Deploying app and MediaMTX..."
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
./scripts/deploy-mediamtx.sh "$ENV"

echo "Rollout status:"
kubectl rollout status deployment/launch-labs-app
