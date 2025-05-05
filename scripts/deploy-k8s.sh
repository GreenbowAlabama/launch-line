#!/bin/bash

# Resolve script base directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
K8S_DIR="$PROJECT_ROOT/k8s"

echo "🚀 Applying Kubernetes manifests from $K8S_DIR..."

kubectl apply -f "$K8S_DIR/deployment.yaml"
kubectl apply -f "$K8S_DIR/service.yaml"

echo "✅ Done. Current resources:"
kubectl get pods
kubectl get svc launch-labs-service
