#!/bin/bash

# Usage:
# ./deploy-with-configmap.sh \
#   --namespace mediamtx \
#   --deployment mediamtx \
#   --configmap mediamtx-config \
#   --configfile k8s/mediamtx.yml

set -e

# Defaults
NAMESPACE="default"
DEPLOYMENT=""
CONFIGMAP=""
CONFIGFILE=""

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --namespace)
      NAMESPACE="$2"
      shift
      shift
      ;;
    --deployment)
      DEPLOYMENT="$2"
      shift
      shift
      ;;
    --configmap)
      CONFIGMAP="$2"
      shift
      shift
      ;;
    --configfile)
      CONFIGFILE="$2"
      shift
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validation
if [[ -z "$DEPLOYMENT" || -z "$CONFIGMAP" || -z "$CONFIGFILE" ]]; then
  echo "Missing required arguments."
  echo "Usage: $0 --namespace <ns> --deployment <name> --configmap <name> --configfile <file>"
  exit 1
fi

# Apply ConfigMap
echo "Updating ConfigMap $CONFIGMAP in namespace $NAMESPACE with file $CONFIGFILE..."
kubectl create configmap "$CONFIGMAP" \
  --namespace "$NAMESPACE" \
  --from-file=mediamtx.yml="$CONFIGFILE" \
  --dry-run=client -o yaml | kubectl apply -f -

# Patch deployment to trigger restart
echo "Patching deployment $DEPLOYMENT to trigger rollout..."
kubectl patch deployment "$DEPLOYMENT" \
  --namespace "$NAMESPACE" \
  -p '{"spec":{"template":{"metadata":{"annotations":{"configmap-update":"'"$(date +%s)'"}}}}}'

echo "✅ ConfigMap updated and deployment restarted."
