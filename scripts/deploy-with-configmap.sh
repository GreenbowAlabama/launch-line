#!/bin/bash

# Usage: ./deploy-with-configmap.sh <app-name> <namespace> <configmap-name> <config-file-path>

APP_NAME=$1
NAMESPACE=$2
CONFIGMAP_NAME=$3
CONFIG_FILE_PATH=$4

if [[ -z "$APP_NAME" || -z "$NAMESPACE" || -z "$CONFIGMAP_NAME" || -z "$CONFIG_FILE_PATH" ]]; then
  echo "Usage: $0 <app-name> <namespace> <configmap-name> <config-file-path>"
  exit 1
fi

# Ensure namespace exists
kubectl get ns "$NAMESPACE" >/dev/null 2>&1 || kubectl create ns "$NAMESPACE"

# Create or update ConfigMap from the specified file
kubectl create configmap "$CONFIGMAP_NAME" \
  --from-file="$CONFIG_FILE_PATH" \
  --namespace "$NAMESPACE" \
  --dry-run=client -o yaml | kubectl apply -f -

# Patch deployment to trigger a rollout if ConfigMap has changed
kubectl patch deployment "$APP_NAME" \
  -n "$NAMESPACE" \
  -p "{\"spec\":{\"template\":{\"metadata\":{\"annotations\":{\"configmap-hash\":\"$(date +%s)\"}}}}}"

# Confirm rollout status
kubectl rollout status deployment "$APP_NAME" -n "$NAMESPACE"
