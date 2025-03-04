#!/bin/bash

echo "Enter your SERPER_API_KEY (from GitHub Secrets):"
read -s SERPER_API_KEY  # Read secret input without echoing it

kubectl delete secret serper-api-key --ignore-not-found
kubectl create secret generic serper-api-key --from-literal=SERPER_API_KEY="$SERPER_API_KEY"

echo "Secret successfully updated in Minikube!"
