# Makefile

.PHONY: start stop port-forward

start:
	@echo "Clearing old port forwards"
	-pkill -f "kubectl port-forward svc/launch-lab-app" || true

	@echo "Deploying Helm chart..."
	helm upgrade --install launch-lab ./charts/launch-lab

	@echo "Waiting for pods..."
	kubectl rollout status deployment/launch-lab-app --namespace default

	@echo "Starting port forwarding..."
	$(MAKE) port-forward

port-forward:
	kubectl port-forward svc/launch-lab-app 5050:5050

stop:
	@echo "Stopping port forwarding..."
	-pkill -f "kubectl port-forward svc/launch-lab-app" || true

	@echo "Uninstalling Helm release..."
	helm uninstall launch-lab || true

	@echo "Deleting ConfigMap (if exists)..."
	kubectl delete configmap launch-lab-config --ignore-not-found