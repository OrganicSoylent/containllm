#!/bin/bash

deploy() {
    read -p "Do you want to deploy $1? (y/n): " choice
    case "$choice" in 
      y|Y )
        echo "Deploying $1..."
        kubectl apply -f $2
        ;;
      * )
        echo "Skipping $1..."
        ;;
    esac
}

deploy "Kubernetes-dashboard @ https://localhost:9100" "kubernetes-dashboard/."
deploy "Ollama" "ollama-deployment/."
deploy "Openweb UI @ http://localhost:9000" "openwebui-deployment/."
deploy "n8n AI-agent @ http://localhost:9200" "n8n-deployment/."