#!/bin/bash

# Usage:
# ./deploy-with-configmap.sh \
#   --namespace mediamtx \
#   --deployment mediamtx \
#   --configmap mediamtx-config \
#   --configfile config/mediamtx.yml

set -e

# Defaults
NAMESPACE=""
DEPLOYMENT=""
CONFIGMAP=""
CONFIGFILE=""

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --namespace)
      NAMESPACE="$2"
      shift 2
      ;;
    --deployment)
      DEPLOYMENT="$2"
      shift 2
      ;;
    --configmap)
      CONFIGMAP="$2"
      shift 2
      ;;
    --configfile)
      CONFIGFILE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate
if [[ -z "$NAMESPACE" || -z "$DEPLOYMENT" || -z "$CONFIGMAP" || -z "$CONFIGFILE" ]]; then
  echo "Missing required arguments."
  echo "Usage: $0 --namespace <ns> --deployment <name> --configmap <name> --configfile <file>"
  exit 1
fi

# Apply updated configmap
echo "Updating ConfigMap $CONFIGMAP in namespace $NAMESPACE with file $CONFIGFILE..."
kubectl create configmap "$CONFIGMAP" \
  --namespace "$NAMESPACE" \
  --from-file=mediamtx.yml="$CONFIGFILE" \
  --dry-run=client -o yaml | kubectl apply -f -

# Trigger deployment restart via annotation patch
echo "Patching deployment $DEPLOYMENT in $NAMESPACE..."
kubectl patch deployment "$DEPLOYMENT" --namespace "$NAMESPACE" -p "$(cat <<EOF
{
  "spec": {
    "template": {
      "metadata": {
        "annotations": {
          "configmap-update": "$(date +%s)"
        }
      }
    }
  }
}
EOF
)"

echo "✅ ConfigMap updated and rollout triggered."