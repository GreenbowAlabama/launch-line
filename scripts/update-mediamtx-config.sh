#!/bin/bash

ENV=$1
RESOURCE_GROUP=${RESOURCE_GROUP:-launch-labs-${ENV}-rg}
K8S_NAMESPACE="mediamtx"
CONFIG_FILE="k8s/mediamtx-configmap.yml"

echo "Applying ConfigMap from $CONFIG_FILE..."
kubectl apply -f "$CONFIG_FILE" --namespace $K8S_NAMESPACE --save-config --record > tmp_output.txt

if grep -q "configured" tmp_output.txt; then
  echo "ConfigMap changed. Restarting MediaMTX deployment..."
  kubectl rollout restart deployment mediamtx -n $K8S_NAMESPACE
else
  echo "No changes to ConfigMap. Skipping deployment restart."
fi

rm -f tmp_output.txt