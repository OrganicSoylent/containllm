#!/bin/bash

echo "1 - creating namespace"

kubectl apply -f crewai-deployment/1-namespace.yaml

echo "2 - creating secrets"
echo "Enter your SERPER_API_KEY:"
read SERPER_API_KEY
export SERPER_API_KEY

# Process the Secret YAML with envsubst before applying
envsubst < crewai-deployment/2-secrets.yaml | kubectl apply -f -

echo "3 - creating configmap"
echo "Enter your CAR_BRAND for the marketing example app:"
read CAR_BRAND
export CAR_BRAND

# Process the ConfigMap YAML with envsubst before applying
envsubst < crewai-deployment/3-configmap.yaml | kubectl apply -f -

echo "4 - creating crewai deployment"

kubectl apply -f crewai-deployment/4-deployment.yaml

echo "5 - creating LoadBalancer"

kubectl apply -f crewai-deployment/5-service.yaml

echo "CrewAI setup completed"