# scripts/install-ingress.sh
#!/bin/bash 

set -e

NAMESPACE="${INGRESS_NAMESPACE:-ingress-nginx}"

kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace "$NAMESPACE" \
  --set controller.publishService.enabled=true